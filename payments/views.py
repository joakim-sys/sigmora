import json
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Order, PaymentSettings
from .providers import NowPaymentsProvider


@csrf_exempt
def nowpayments_webhook_view(request: HttpRequest) -> HttpResponse:
    """
    Receives Instant Payment Notifications (IPN) from NOWPayments.
    """
    try:
        signature = request.headers.get("x-nowpayments-sig")
        payload = json.loads(request.body)
    except (json.JSONDecodeError, KeyError):
        return HttpResponse("Invalid request", status=400)

    # Verify the signature
    payment_settings = PaymentSettings.for_request(request)
    provider = NowPaymentsProvider(
        api_key="", ipn_secret_key=payment_settings.nowpayments_ipn_secret_key
    )

    if not provider.verify_webhook_signature(payload, signature):
        return HttpResponse("Invalid signature", status=403)

    # Process the verified webhook
    order_id = payload.get("order_id")
    payment_status = payload.get("payment_status")

    try:
        order = Order.objects.get(order_id=order_id)

        if payment_status == "finished":
            if order.status == Order.OrderStatus.PENDING:
                order.status = Order.OrderStatus.PAID
                order.nowpayments_payment_id = payload.get("payment_id")
                order.paid_at = timezone.now()
                order.save()
                # TODO: Send "Payment Received" email to client and admin

        elif payment_status in ["expired", "failed"]:
            if order.status == Order.OrderStatus.PENDING:
                order.status = (
                    Order.OrderStatus.FAILED
                    if payment_status == "failed"
                    else Order.OrderStatus.EXPIRED
                )
                order.save()
                # TODO: Send "Payment Failed" email

    except Order.DoesNotExist:
        # This can happen if NOWPayments sends a notification for an order not in our DB
        # You might want to log this for investigation
        pass

    return HttpResponse("Webhook processed successfully", status=200)


def payment_success_view(request):
    # This is the page the user sees after a successful payment
    return render(request, "payments/payment_success.html")


def payment_failure_view(request):
    # This is the page the user sees after a failed or cancelled payment
    return render(request, "payments/payment_failure.html")
