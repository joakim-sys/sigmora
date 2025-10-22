# payments/models.py
import uuid
from django.db import models
from django.conf import settings
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

@register_setting
class PaymentSettings(BaseSiteSetting):
    nowpayments_api_key = models.CharField(max_length=255, blank=True)
    nowpayments_ipn_secret_key = models.CharField(max_length=255, blank=True)
    support_email = models.EmailField(blank=True, help_text="The email address for customer support inquiries.")
    
    panels = [
        MultiFieldPanel([
            FieldPanel("nowpayments_api_key"),
            FieldPanel("nowpayments_ipn_secret_key"),
        ], heading="NOWPayments API Credentials"),
         MultiFieldPanel([
            FieldPanel("support_email"),
        ], heading="Support Information"),
    ]
    class Meta:
        verbose_name = "Payment Settings"

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        FAILED = 'failed', 'Failed'
        EXPIRED = 'expired', 'Expired'

    # Links to the products app
    product = models.ForeignKey('products.ProductPage', on_delete=models.PROTECT)
    pricing_tier = models.ForeignKey('products.PricingTier', on_delete=models.PROTECT)
    
    # User and form details
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    
    # Financial and Transactional Details
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=36, unique=True, editable=False, default=uuid.uuid4)
    
    # NOWPayments specific fields
    nowpayments_invoice_id = models.CharField(max_length=255, blank=True, null=True)
    nowpayments_payment_id = models.CharField(max_length=255, blank=True, null=True)

    # Status and Timestamps
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)


    # --- Replace the old 'preferred_platforms' field ---
    platform_choice = models.CharField(max_length=50, help_text="The platform selected by the user.",null=True)

    # --- Add New Essential Project Fields ---
    project_name = models.CharField(max_length=255, help_text="The requested name for the application.",null=True)
    core_functionality = models.TextField(help_text="A summary of the project's main purpose and features.",null=True)
    brand_details = models.TextField(blank=True, help_text="Client notes on branding, colors, logos, etc.",null=True)


    def __str__(self):
        return f"Order {self.order_id}"