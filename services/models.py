from django.db import models

from wagtail.models import Page, Orderable
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.fields import StreamField
from modelcluster.fields import ParentalKey

from wagtail.blocks import RichTextBlock

from base.blocks import BaseStreamBlock
from services.blocks import (
    ImageBlock,
    FeatureGridBlock,
    ImageUrlBlock,
    WFeatureCardBlock,
    WFeatureItemBlock,
    ProcessListBlock,
)
from contact.models import ContactPage


class ServicePage(Page):

    testimonial = models.ForeignKey(
        "base.Testimonial",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional: select a testimonial to display in the sidebar.",
    )

    contact_form = models.ForeignKey(
        ContactPage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional: select a form to display in the sidebar.",
    )

    # The main content area, built with a variety of reusable blocks.
    body = StreamField(
        [
            (
                "rich_text",
                RichTextBlock(
                    icon="pilcrow",
                    label="Rich Text",
                    features=[
                        "h2",
                        "h3",
                        "h4",
                        "bold",
                        "italic",
                        "link",
                        "ol",
                        "ul",
                        "hr",
                    ],
                ),
            ),
            ("image", ImageBlock()),
            ('image_url', ImageUrlBlock()),
            ("feature_grid", FeatureGridBlock()),
            ("process_list", ProcessListBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        MultiFieldPanel(
            [
                InlinePanel("service_details", label="Detail"),
            ],
            heading="Service Details",
        ),
        FieldPanel("testimonial"),
        PageChooserPanel("contact_form", "contact.ContactPage"),
    ]


class ServiceDetail(Orderable):
    """A single detail/fact for the service, editable inline on ServicePage."""

    page = ParentalKey(
        ServicePage,
        on_delete=models.CASCADE,
        related_name="service_details",
    )
    fact_label = models.CharField(max_length=100, help_text="e.g. 'Duration'")
    fact_value = models.CharField(max_length=100, help_text="e.g. '3-6 Months'")

    panels = [
        FieldPanel("fact_label"),
        FieldPanel("fact_value"),
    ]


class WhyUsPage(Page):
    """A page to represent the 'Why Us' section."""

    # Section Title
    section_title = models.CharField(max_length=255, default="Why Us")
    section_subtitle = models.TextField(blank=True)

    # Feature Cards - using a ListBlock of StructBlocks
    feature_cards = StreamField(
        [("feature_card", WFeatureCardBlock())], use_json_field=True, blank=True
    )

    # Feature Showcase
    showcase_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    showcase_title = models.CharField(max_length=255, blank=True)
    showcase_lead_text = models.TextField(blank=True)

    # Feature List - using a ListBlock of StructBlocks
    feature_list = StreamField(
        [("feature_item", WFeatureItemBlock())], use_json_field=True, blank=True
    )

    # Call to Action Buttons
    primary_cta_text = models.CharField(
        max_length=100, blank=True, default="Start Your Project"
    )
    primary_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )
    secondary_cta_text = models.CharField(
        max_length=100, blank=True, default="View Portfolio"
    )
    secondary_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )

    content_panels = Page.content_panels + [
        FieldPanel("section_title"),
        FieldPanel("section_subtitle"),
        FieldPanel("feature_cards"),
        FieldPanel("showcase_image"),
        FieldPanel("showcase_title"),
        FieldPanel("showcase_lead_text"),
        FieldPanel("feature_list"),
        FieldPanel("primary_cta_text"),
        FieldPanel("primary_cta_link"),
        FieldPanel("secondary_cta_text"),
        FieldPanel("secondary_cta_link"),
    ]
