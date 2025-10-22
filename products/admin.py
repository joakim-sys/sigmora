# # products/admin.py
# from django.contrib import admin
# from .models import Order


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = (
#         "order_id",
#         "product",
#         "pricing_tier",
#         "email",
#         "status",
#         "created_at",
#     )
#     list_filter = ("status", "created_at")
#     search_fields = ("order_id", "email", "full_name")
#     readonly_fields = ("order_id", "created_at")
