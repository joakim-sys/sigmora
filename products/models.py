import uuid
from django.conf import settings
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.models import Page, Orderable
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.snippets.models import register_snippet
from wagtail.images.blocks import ImageChooserBlock

from products.blocks import AccordionBlock

# ===================================================================
# 1. CATEGORY SNIPPET (For organizing products)
# ===================================================================


@register_snippet
class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Product Categories"


# ===================================================================
# 2. PRODUCT DETAIL PAGE and its repeatable components
# ===================================================================


class ProductImage(Orderable):
    """A repeatable image for the product's main slider gallery."""

    page = ParentalKey(
        "ProductPage", on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )

    image_url = models.URLField(max_length=255, null=True, blank=True)

    panels = [FieldPanel("image"), FieldPanel("image_url")]


class ProductTechBadge(Orderable):
    """A repeatable tech stack badge."""

    page = ParentalKey(
        "ProductPage", on_delete=models.CASCADE, related_name="tech_stack"
    )
    name = models.CharField(max_length=50)

    panels = [FieldPanel("name")]


class TierFeature(Orderable):
    """A single feature for a pricing tier."""

    tier = ParentalKey("PricingTier", on_delete=models.CASCADE, related_name="features")
    text = models.CharField(max_length=255)
    is_included = models.BooleanField(
        default=True,
        help_text="Check if this feature is included (shows a checkmark). Uncheck for an 'X'.",
    )

    panels = [FieldPanel("text"), FieldPanel("is_included")]


class PricingTier(ClusterableModel, Orderable):
    """A pricing tier for a ProductPage."""

    page = ParentalKey(
        "ProductPage", on_delete=models.CASCADE, related_name="pricing_tiers"
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_suffix = models.CharField(max_length=50, default="/ month")
    is_featured = models.BooleanField(
        default=False, help_text="Check to apply the 'featured' styling to this tier."
    )
    nowpayment_url = models.URLField(max_length=100, null=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("price"),
        FieldPanel("nowpayment_url"),
        FieldPanel("price_suffix"),
        FieldPanel("is_featured"),
        InlinePanel("features", label="Tier Feature"),
    ]

    def __str__(self):
        return self.name


class ProductPage(Page, ClusterableModel):
    """The main detail page for a single product."""

    # --- Metadata ---
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    project_date = models.DateField("Project date", null=True, blank=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    project_website = models.URLField(blank=True, null=True)

    # --- Main Content ---
    lead_paragraph = models.TextField(
        help_text="The introductory paragraph below the title.", null=True, blank=True
    )

    # Using StreamField for the accordion and other rich content
    body = StreamField(
        [
            ("accordion", AccordionBlock()),
            ("rich_text", blocks.RichTextBlock(icon="pilcrow")),
            ("image", ImageChooserBlock(icon="image")),
        ],
        use_json_field=True,
        blank=True,
    )

    # --- Pricing Section ---
    pricing_title = models.CharField(
        max_length=100, default="Pricing", null=True, blank=True
    )
    pricing_subtitle = models.TextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("category"),
                FieldPanel("project_date"),
                FieldPanel("client_name"),
                FieldPanel("project_website"),
            ],
            heading="Project Metadata",
        ),
        InlinePanel("gallery_images", label="Gallery Image", min_num=1),
        InlinePanel("tech_stack", label="Tech Stack Badge"),
        MultiFieldPanel(
            [
                FieldPanel("lead_paragraph"),
                FieldPanel("body"),
            ],
            heading="Project Overview",
        ),
        MultiFieldPanel(
            [
                FieldPanel("pricing_title"),
                FieldPanel("pricing_subtitle"),
                InlinePanel("pricing_tiers", label="Pricing Tier", max_num=3),
            ],
            heading="Pricing Section",
        ),
    ]


# ===================================================================
# 3. PRODUCT LISTING PAGE
# ===================================================================


class ProductListingPage(Page):
    """Page to list all the products."""

    introduction = models.TextField(blank=True)

    # --- Product CTA Snippet Fields ---
    product_cta_title = models.CharField(
        max_length=100, blank=True, default="Ready to start your next project?"
    )
    product_cta_subtitle = models.TextField(
        blank=True, default="Let's work together to bring your digital vision to life"
    )

    # --- CTA Buttons ---
    product_cta_primary_text = models.CharField(
        max_length=50, blank=True, default="Start a Project"
    )
    product_cta_primary_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Choose a page for the primary button (e.g., Contact Page).",
    )

    product_cta_secondary_text = models.CharField(
        max_length=50, blank=True, default="View All Work"
    )
    product_cta_secondary_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Choose a page for the secondary button (e.g., Pricing Page).",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        # Products CTA Panel
        MultiFieldPanel(
            [
                FieldPanel("product_cta_title"),
                FieldPanel("product_cta_subtitle"),
                MultiFieldPanel(
                    [
                        FieldPanel("product_cta_primary_text"),
                        PageChooserPanel("product_cta_primary_link"),
                    ],
                    heading="Primary Button",
                ),
                MultiFieldPanel(
                    [
                        FieldPanel("product_cta_secondary_text"),
                        PageChooserPanel("product_cta_secondary_link"),
                    ],
                    heading="Secondary Button",
                ),
            ],
            heading="Product CTA Section",
            classname="collapsible collapsed",
        ),
    ]

    subpage_types = ["products.ProductPage"]

    def get_products(self):
        products = (
            ProductPage.objects.live().descendant_of(self).order_by("-project_date")
        )
        return products

    def get_categories(self):
        categories = ProductCategory.objects.all()
        return categories

    def get_context(self, request):
        context = super().get_context(request)
        # Get all published ProductPages that are children of this page
        products = (
            ProductPage.objects.live().descendant_of(self).order_by("-project_date")
        )
        categories = ProductCategory.objects.all()
        context["products"] = products
        context["categories"] = categories
        return context
