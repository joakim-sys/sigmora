from django.db import models
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
    InlinePanel,
)
from wagtail.models import Page, PreviewableMixin, DraftStateMixin, RevisionMixin
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey

from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)
from modelcluster.models import ClusterableModel
from wagtail.blocks import RichTextBlock, RawHTMLBlock
from base.blocks import ImageWithCaptionBlock, LinkColumnBlock, QuoteBlock
from portfolio.blocks import HeadingBlock


@register_snippet
class Testimonial(models.Model):
    """A reusable testimonial snippet."""

    quote = models.TextField()
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=100, blank=True)
    author_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("quote"),
        MultiFieldPanel(
            [
                FieldPanel("author_name"),
                FieldPanel("author_title"),
                FieldPanel("author_image"),
            ],
            heading="Author",
        ),
    ]

    def __str__(self):
        return f""""{self.quote}" - {self.author_name}"""


class StandardPage(Page):
    """
    A flexible standard page with a subtitle and a customizable StreamField body.
    """
    # This field is for the subtitle that appears under the main title.
    subtitle = models.TextField(
        blank=True,
        help_text="A short subtitle that appears under the main page title."
    )

    # This is the main content area, using StreamField for maximum flexibility.
    body = StreamField([
        ('rich_text', RichTextBlock(
            icon='pilcrow',
            label='Rich Text',
            features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr']
        )),
        ('heading', HeadingBlock()),
        ('image', ImageWithCaptionBlock()),
        ('quote', QuoteBlock()),
        ('html', RawHTMLBlock(
            icon='code',
            label='Raw HTML'
        )),
    ], use_json_field=True, blank=True, help_text="The main content of the page, built from a variety of blocks.")

    # Define which fields are editable in the Wagtail admin.
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]

    # You can also add promote_panels or settings_panels if needed.
    # promote_panels = Page.promote_panels





@register_snippet
class Header(PreviewableMixin, DraftStateMixin, RevisionMixin, ClusterableModel):
    """
    Snippet representing the site header.

    Fields map to items present in `templates/includes/header.html`:
    - optional logo image and alt text
    - optional site title override
    - CTA (text + internal page or external URL)

    This snippet is previewable and supports draft state.
    """

    site_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional override for the site title shown in the header",
    )

    # logo = models.ForeignKey(
    #     "wagtailimages.Image",
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name="+",
    # )

    logo_alt = models.CharField(
        max_length=255, blank=True, help_text="Alt text for the logo image"
    )

    cta_text = models.CharField(
        max_length=100, blank=True, help_text="Text for the CTA button"
    )
    cta_page = models.ForeignKey(
        Page, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    cta_url = models.URLField(
        blank=True, help_text="External URL for the CTA button (used if no page chosen)"
    )

    panels = [
        FieldPanel("site_title"),
        FieldPanel("logo_alt"),
        MultiFieldPanel(
            [
                FieldPanel("cta_text"),
                PageChooserPanel("cta_page"),
                FieldPanel("cta_url"),
            ],
            heading="CTA",
        ),
    ]

    def __str__(self):
        return self.site_title or (self.logo_alt or "Header snippet")

    @property
    def cta_link(self):
        """Return the best URL for the CTA: internal page first, then external URL, then fallback anchor."""
        if self.cta_page:
            try:
                return self.cta_page.url
            except Exception:
                return None
        if self.cta_url:
            return self.cta_url
        return "#about"

    def get_preview_template(self, request, mode_name=None):
        """Return the template used to preview the header snippet in the admin."""
        return "base/preview/header.html"


@register_setting(icon="cog")
class GenericSettings(ClusterableModel, BaseGenericSetting):
    x_url = models.URLField(verbose_name="X URL", blank=True)
    facebook_url = models.URLField(verbose_name="Facebook URL", blank=True)
    instagram_url = models.URLField(verbose_name="Instagram URL", blank=True)
    linkedin_url = models.URLField(verbose_name="LinkedIn URL", blank=True)
    tiktok_url = models.URLField(verbose_name="Tiktok URL", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("x_url"),
                FieldPanel("facebook_url"),
                FieldPanel("instagram_url"),
                FieldPanel("linkedin_url"),
                FieldPanel("tiktok_url"),
            ],
            "Social settings",
        )
    ]


@register_setting(icon="site")
class SiteSettings(BaseSiteSetting):
    title_suffix = models.CharField(
        verbose_name="Title suffix",
        max_length=255,
        help_text="The suffix for the title meta tag e.g. ' | Sigmora'",
        default="Sigmora",
    )

    panels = [
        FieldPanel("title_suffix"),
    ]


@register_setting
class FooterSettings(ClusterableModel, PreviewableMixin, BaseSiteSetting):
    """
    The model for the site-wide footer settings.
    ClusterableModel is used to support the ParentalKey for social links.
    """

    # --- About Section ---
    site_name = models.CharField(
        max_length=255,
        default="Sigmora",
        help_text="The name of the site, displayed in the footer.",
    )
    about_text = RichTextField(
        features=["bold", "italic", "link"],
        help_text="The contact information or 'about' text.",
    )

    # --- Link Columns Section (using StreamField) ---
    footer_links = StreamField(
        [
            ("column", LinkColumnBlock()),
        ],
        use_json_field=True,
        blank=True,
        help_text="Add columns of links to the footer.",
    )

    # --- Copyright Section ---
    copyright_text = models.CharField(max_length=255, blank=True, default="Copyright")
    credits_text = RichTextField(
        features=["link"],
        blank=True,
        default="Designed by <a>Sigmora</a>",
        help_text="The credits line at the bottom of the footer.",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("site_name"),
                FieldPanel("about_text"),
                InlinePanel("social_links", label="Social Media Link"),
            ],
            heading="About and Socials",
        ),
        MultiFieldPanel(
            [
                FieldPanel("footer_links"),
            ],
            heading="Footer Link Columns",
        ),
        MultiFieldPanel(
            [
                FieldPanel("copyright_text"),
                FieldPanel("credits_text"),
            ],
            heading="Copyright and Credits",
        ),
    ]

    def get_preview_template(self, request, mode_name):
        return "base.html"

    class Meta:
        verbose_name = "Footer Settings"


class SocialLink(Orderable):
    """A repeatable model for social media links in the footer."""

    footer_settings = ParentalKey(
        FooterSettings, on_delete=models.CASCADE, related_name="social_links"
    )
    url = models.URLField(help_text="The full URL of the social media profile.")
    icon_class = models.CharField(
        max_length=100, help_text="The Bootstrap Icon class (e.g., 'bi bi-twitter-x')."
    )

    panels = [
        FieldPanel("url"),
        FieldPanel("icon_class"),
    ]
