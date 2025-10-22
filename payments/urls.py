from django.urls import path
from . import views

app_name = "payments"
urlpatterns = [
    path(
        "webhook/nowpayments/",
        views.nowpayments_webhook_view,
        name="nowpayments_webhook",
    ),
    path("success/", views.payment_success_view, name="payment_success"),
    path("failure/", views.payment_failure_view, name="payment_failure"),
]
