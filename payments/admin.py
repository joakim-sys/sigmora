from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "product",
        "email",
        "status",
        "price_at_purchase",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("order_id", "email")
