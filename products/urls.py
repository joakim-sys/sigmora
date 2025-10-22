from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    # This URL will handle the creation of a new order for a specific product and tier
    path(
        "order/create/<int:product_id>/<int:tier_id>/",
        views.create_order_view,
        name="create_order",
    ),
]
