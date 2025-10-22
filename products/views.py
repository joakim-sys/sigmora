from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from wagtail.models import Site

from .models import ProductPage, PricingTier
from .forms import OrderForm

# Import the payment provider and settings from the payments app
from payments.models import Order, PaymentSettings
from payments.providers import NowPaymentsProvider


def create_order_view(request, product_id, tier_id):
    product = get_object_or_404(ProductPage, id=product_id)
    tier = get_object_or_404(PricingTier, id=tier_id, page=product)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create the order in a 'pending' state
            order = Order.objects.create(
                # product=product,
                # pricing_tier=tier,
                # price_at_purchase=tier.price,
                # full_name=form.cleaned_data["full_name"],
                # email=form.cleaned_data["email"],

                    product=product,
                    pricing_tier=tier,
                    price_at_purchase=tier.price,
                    payment_provider='nowpayments', # Or your provider
                    
                    # Map the new form fields to the model fields
                    full_name=form.cleaned_data['full_name'],
                    email=form.cleaned_data['email'],
                    platform_choice=form.cleaned_data['platform_choice'],
                    project_name=form.cleaned_data['project_name'],
                    core_functionality=form.cleaned_data['core_functionality'],
                    brand_details=form.cleaned_data['brand_details'],
            )

            # Initiate payment with NOWPayments
            payment_settings = PaymentSettings.for_request(request)
            provider = NowPaymentsProvider(
                api_key=payment_settings.nowpayments_api_key,
                ipn_secret_key=payment_settings.nowpayments_ipn_secret_key,
            )

            try:
                redirect_url = provider.initiate_payment(order, request)
                return redirect(redirect_url)
            except Exception as e:
                order.status = Order.OrderStatus.FAILED
                order.save()
                messages.error(
                    request,
                    "Could not connect to the payment gateway. Please try again.",
                )
                return redirect(product.get_url())
    else:
        form = OrderForm()

    return render(
        request,
        "products/order_form.html",
        {"product": product, "tier": tier, "form": form},
    )
