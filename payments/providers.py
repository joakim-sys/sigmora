# payments/providers.py
import json
import hmac
import hashlib
import requests
from abc import ABC, abstractmethod
from django.urls import reverse


class AbstractPaymentProvider(ABC):
    @abstractmethod
    def initiate_payment(self, order, request):
        pass


class NowPaymentsProvider(AbstractPaymentProvider):
    def __init__(self, api_key, ipn_secret_key):
        self.api_key = api_key
        self.ipn_secret_key = ipn_secret_key
        self.base_url = "https://api.nowpayments.io/v1"

    def initiate_payment(self, order, request):
        """
        Implements the "Create Invoice" flow from the NOWPayments documentation.
        """
        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}

        # Build the URLs for callbacks and redirects
        ipn_callback_url = request.build_absolute_uri(
            reverse("payments:nowpayments_webhook")
        )
        success_url = request.build_absolute_uri(
            reverse("payments:payment_success")
        )  # We will create this URL
        cancel_url = request.build_absolute_uri(
            reverse("payments:payment_failure")
        )  # We will create this URL

        payload = {
            "price_amount": float(order.price_at_purchase),
            "price_currency": "usd",  # Or your site's main currency
            "order_id": str(order.order_id),
            "order_description": f"Order for {order.product.title} - {order.pricing_tier.name}",
            "ipn_callback_url": ipn_callback_url,
            "success_url": success_url,
            "cancel_url": cancel_url,
        }

        response = requests.post(
            f"{self.base_url}/invoice", json=payload, headers=headers
        )
        response.raise_for_status()  # Will raise an error for non-2xx responses

        data = response.json()

        # Save the invoice ID to our order for tracking
        order.nowpayments_invoice_id = data.get("id")
        order.save()

        # Return the URL for the user to pay
        return data.get("invoice_url")

    def verify_webhook_signature(self, request_body, signature_header):
        """
        Verifies the HMAC-SHA512 signature from the webhook request.
        This is a critical security measure.
        """
        try:
            # Recreate the signature from the payload
            sorted_payload = json.dumps(
                request_body, separators=(",", ":"), sort_keys=True
            )
            digest = hmac.new(
                key=self.ipn_secret_key.encode(),
                msg=sorted_payload.encode(),
                digestmod=hashlib.sha512,
            )
            expected_signature = digest.hexdigest()

            # Compare with the signature from the header
            return hmac.compare_digest(expected_signature, signature_header)
        except Exception:
            return False
