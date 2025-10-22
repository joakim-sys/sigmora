
from abc import ABC, abstractmethod
import requests
from django.urls import reverse


class AbstractPaymentProvider(ABC):
    @abstractmethod
    def initiate_payment(self, order, request):
        pass

    @abstractmethod
    def verify_payment(self, transaction_id):
        pass


class FlutterwaveProvider(AbstractPaymentProvider):
    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key
        self.base_url = "https://api.flutterwave.com/v3"

    def initiate_payment(self, order, request):
        headers = {"Authorization": f"Bearer {self.secret_key}"}
        # The callback URL tells Flutterwave where to send the user back to
        callback_url = request.build_absolute_uri(reverse("payments:payment_callback"))

        payload = {
            "tx_ref": str(order.order_id),
            "amount": str(order.price_at_purchase),
            "currency": "USD",
            "redirect_url": callback_url,
            "customer": {"email": order.email, "name": order.full_name},
            "customizations": {"title": f"{order.product.title}"},
        }

        response = requests.post(
            f"{self.base_url}/payments", json=payload, headers=headers
        )
        response.raise_for_status()
        return response.json()["data"]["link"]

    def verify_payment(self, transaction_id):
        headers = {"Authorization": f"Bearer {self.secret_key}"}
        url = f"{self.base_url}/transactions/{transaction_id}/verify"

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        res_json = response.json()

        return res_json["data"]["status"] == "successful"
