from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable


class ContactMethod(Orderable):
    """A repeatable contact method card (Email, Phone, Office)."""

    page = ParentalKey(
        "ContactPage", on_delete=models.CASCADE, related_name="contact_methods"
    )
    icon_class = models.CharField(
        max_length=100,
        help_text="The Bootstrap Icon class (e.g., 'bi bi-envelope-at').",
    )
    title = models.CharField(max_length=100)
    details = models.CharField(
        max_length=255,
        help_text="The contact detail (e.g., email, phone number, or address).",
    )
    response_time = models.CharField(
        max_length=100, help_text="The small text below the detail."
    )

    panels = [
        FieldPanel("icon_class"),
        FieldPanel("title"),
        FieldPanel("details"),
        FieldPanel("response_time"),
    ]


class ContactStat(Orderable):
    """A repeatable stat item for the contact page."""

    page = ParentalKey(
        "ContactPage", on_delete=models.CASCADE, related_name="contact_stats"
    )
    number = models.CharField(max_length=20)
    label = models.CharField(max_length=100)

    panels = [
        FieldPanel("number"),
        FieldPanel("label"),
    ]


class ContactSocialLink(Orderable):
    """A repeatable social media link."""

    page = ParentalKey(
        "ContactPage", on_delete=models.CASCADE, related_name="social_links"
    )
    icon_class = models.CharField(
        max_length=100, help_text="The Bootstrap Icon class (e.g., 'bi bi-linkedin')."
    )
    url = models.URLField()

    panels = [
        FieldPanel("icon_class"),
        FieldPanel("url"),
    ]


class FormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    # Section title and subtitle
    contact_section_title = models.CharField(max_length=255, blank=True)
    contact_section_subtitle = models.TextField(blank=True)

    # Form header
    form_header_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text="Bootstrap icon class e.g. bi bi-chat-dots-fill",
    )
    form_header_title = models.CharField(max_length=255, blank=True)
    form_header_paragraph = models.TextField(blank=True)

    # Info header
    info_header_title = models.CharField(max_length=255, blank=True)
    info_header_text = models.TextField(blank=True)

    # --- Social Connect Title ---
    social_connect_title = models.CharField(
        max_length=100, blank=True, default="Connect With Us"
    )

    submit_button_txt = models.CharField(
        max_length=255, blank=True, default="Get a Quote"
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel(
            [
                FieldPanel("contact_section_title"),
                FieldPanel("contact_section_subtitle"),
            ],
            heading="Section Title",
        ),
        MultiFieldPanel(
            [
                FieldPanel("form_header_icon"),
                FieldPanel("form_header_title"),
                FieldPanel("form_header_paragraph"),
            ],
            heading="Form Header",
        ),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldPanel("to_address"),
                FieldPanel("from_address"),
                FieldPanel("subject"),
            ],
            "Email",
        ),
        # Add a new panel for all the contact info fields
        MultiFieldPanel(
            [
                FieldPanel("info_header_title"),
                FieldPanel("info_header_text"),
                InlinePanel(
                    "contact_methods", label="Contact Method Card", min_num=1, max_num=3
                ),
                InlinePanel("contact_stats", label="Info Stat", min_num=1, max_num=3),
                FieldPanel("social_connect_title"),
                InlinePanel("social_links", label="Social Link"),
            ],
            heading="Contact Info Area",
            classname="collapsible",
        ),
        FieldPanel("submit_button_txt"),
    ]
