from django.db import models
from django import forms

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel, ParentalManyToManyField

from wagtail.models import Page, Orderable
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.fields import RichTextField


class HeroStat(Orderable):
    """A repeatable stat item for the hero section."""

    # This links the stat back to the HomePage. The related_name is how we'll access it.
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="hero_stats")

    stat_number = models.IntegerField(help_text="The number to count up to.", default=0)
    stat_label = models.CharField(
        max_length=100, help_text="The text label for the number.", default="Stat Label"
    )

    panels = [
        FieldPanel("stat_number"),
        FieldPanel("stat_label"),
    ]


class AboutFeature(Orderable):
    """A repeatable feature item for the About section's bulleted list."""

    page = ParentalKey(
        "HomePage", on_delete=models.CASCADE, related_name="about_features"
    )
    text = models.CharField(
        max_length=255,
        help_text="The text for a single feature bullet point.",
        default="About Text",
    )

    panels = [FieldPanel("text")]


class AboutStat(Orderable):
    """A repeatable stat for the card in the About section."""

    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="about_stats")
    number = models.CharField(
        max_length=20,
        help_text="The stat number or text (e.g., '20+' or '500+').",
        default="0",
    )
    label = models.CharField(
        max_length=100,
        help_text="The label for the stat (e.g., 'Years of Expertise').",
        default="Stat Label",
    )

    panels = [
        FieldPanel("number"),
        FieldPanel("label"),
    ]


class ServiceCard(Orderable):
    """A repeatable service card for the Services section."""

    page = ParentalKey(
        "HomePage", on_delete=models.CASCADE, related_name="service_cards"
    )

    icon_class = models.CharField(
        max_length=100, help_text="The Bootstrap Icon class (e.g., 'bi bi-palette')."
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    link_page = models.ForeignKey(
        "services.ServicePage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Choose a page to link to for this service (e.g., a Service Detail Page).",
    )

    # Fields for the optional badge
    show_badge = models.BooleanField(
        default=False, help_text="Check to display a badge on this card."
    )
    badge_text = models.CharField(
        max_length=50,
        blank=True,
        help_text="Text for the badge (e.g., 'Most Popular').",
    )

    panels = [
        FieldPanel("icon_class"),
        FieldPanel("title"),
        FieldPanel("description"),
        PageChooserPanel("link_page"),
        MultiFieldPanel(
            [
                FieldPanel("show_badge"),
                FieldPanel("badge_text"),
            ],
            heading="Optional Badge",
        ),
    ]


class HomePage(Page, ClusterableModel):
    # --- Hero Section Fields ---
    hero_heading = models.CharField(
        max_length=255, blank=True, help_text="The main heading for the hero section."
    )
    hero_subheading = models.TextField(
        blank=True, help_text="The paragraph of text below the main heading."
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The main visual for the hero section.",
    )

    # --- Hero CTA Buttons ---
    hero_primary_cta_text = models.CharField(
        max_length=100, blank=True, default="Get Started"
    )
    hero_primary_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The page to link to for the primary button.",
    )

    hero_secondary_cta_text = models.CharField(
        max_length=100, blank=True, default="Our Work"
    )
    hero_secondary_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The page to link to for the secondary button.",
    )

    # About section fields
    about_subtitle = models.CharField(
        max_length=100,
        blank=True,
        help_text="The small subtitle (e.g., 'Discover Our Story').",
    )
    about_title = models.CharField(
        max_length=255, blank=True, help_text="The main title for the About section."
    )
    about_text = RichTextField(
        blank=True,
        features=["bold", "italic", "link"],
        help_text="The main paragraph of text.",
    )

    about_main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The large, primary image for the composition.",
    )
    about_secondary_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The smaller, secondary image.",
    )

    # --- About CTA Button ---
    about_cta_text = models.CharField(
        max_length=100, blank=True, default="Discover More"
    )
    about_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The page to link to for the button.",
    )

    # --- Services Section Fields ---
    services_title = models.CharField(max_length=100, blank=True, default="Services")
    services_subtitle = models.TextField(
        blank=True, help_text="The subtitle for the services section."
    )

    # --- Services CTA Fields ---
    services_cta_title = models.CharField(
        max_length=100, blank=True, default="Ready to Transform Your Digital Presence?"
    )
    services_cta_subtitle = models.TextField(
        blank=True,
        default="Let's discuss your project and create something amazing together",
    )
    services_cta_button_text = models.CharField(
        max_length=50, blank=True, default="Get Started Today"
    )
    services_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The page to link the main CTA button to.",
    )

    # Products
    products_link = models.ForeignKey(
        "products.ProductListingPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The page to link the main CTA button to.",
    )

    # Portfolio section fields
    # portfolio_title = models.CharField(max_length=255, blank=True)
    # portfolio_subtitle = models.TextField(blank=True)

    # portfolio_projects = ParentalManyToManyField("products.ProductPage", blank=True)

    # --- Portfolio CTA Snippet Fields ---
    # portfolio_cta_title = models.CharField(
    #     max_length=100, blank=True, default="Ready to start your next project?"
    # )
    # portfolio_cta_subtitle = models.TextField(
    #     blank=True, default="Let's work together to bring your digital vision to life"
    # )

    # --- CTA Buttons ---
    # portfolio_cta_primary_text = models.CharField(
    #     max_length=50, blank=True, default="Start a Project"
    # )
    # portfolio_cta_primary_link = models.ForeignKey(
    #     "wagtailcore.Page",
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name="+",
    #     help_text="Choose a page for the primary button (e.g., Contact Page).",
    # )

    # portfolio_cta_secondary_text = models.CharField(
    #     max_length=50, blank=True, default="View All Work"
    # )
    # portfolio_cta_secondary_link = models.ForeignKey(
    #     "wagtailcore.Page",
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name="+",
    #     help_text="Choose a page for the secondary button (e.g., Portfolio Page).",
    # )

    #  Why Us Section
    featured_why_us_section = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text='Choose a "Why Us" page to feature on the homepage.',
    )

    def featured_services(self):
        return self.services.all()

    content_panels = Page.content_panels + [
        # Hero Panel
        MultiFieldPanel(
            [
                FieldPanel("hero_heading"),
                FieldPanel("hero_subheading"),
                FieldPanel("hero_image"),
                MultiFieldPanel(
                    [
                        FieldPanel("hero_primary_cta_text"),
                        PageChooserPanel("hero_primary_cta_link"),
                    ],
                    heading="Primary Button",
                ),
                MultiFieldPanel(
                    [
                        FieldPanel("hero_secondary_cta_text"),
                        PageChooserPanel("hero_secondary_cta_link"),
                    ],
                    heading="Secondary Button",
                ),
                # Add the InlinePanel for the repeatable stats
                InlinePanel("hero_stats", label="Hero Stat", min_num=1, max_num=3),
            ],
            heading="Hero Section",
            classname="collapsible collapsed",
        ),
        # About Section Panel
        MultiFieldPanel(
            [
                FieldPanel("about_subtitle"),
                FieldPanel("about_title"),
                FieldPanel("about_text"),
                FieldPanel("about_main_image"),
                FieldPanel("about_secondary_image"),
                MultiFieldPanel(
                    [
                        FieldPanel("about_cta_text"),
                        PageChooserPanel("about_cta_link"),
                    ],
                    heading="CTA Button",
                ),
                InlinePanel(
                    "about_features", label="Feature Item", min_num=1, max_num=4
                ),
                InlinePanel("about_stats", label="Stat Item", min_num=2, max_num=2),
            ],
            heading="About Section",
            classname="collapsible collapsed",
        ),
        # Services Panel
        MultiFieldPanel(
            [
                FieldPanel("services_title"),
                FieldPanel("services_subtitle"),
                InlinePanel("service_cards", label="Service Card", min_num=1),
                MultiFieldPanel(
                    [
                        FieldPanel("services_cta_title"),
                        FieldPanel("services_cta_subtitle"),
                        FieldPanel("services_cta_button_text"),
                        PageChooserPanel("services_cta_link"),
                    ],
                    heading="Call to Action Section",
                ),
            ],
            heading="Services Section",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [PageChooserPanel("products_link")],
            heading="Products",
        ),
        # MultiFieldPanel(
        #     [
        #         # FieldPanel("portfolio_title"),
        #         # FieldPanel("portfolio_subtitle"),
        #         # FieldPanel("portfolio_projects", widget=forms.CheckboxSelectMultiple),
        #
        # Add a new panel for the Portfolio CTA
        #         MultiFieldPanel(
        #             [
        #                 FieldPanel("portfolio_cta_title"),
        #                 FieldPanel("portfolio_cta_subtitle"),
        #                 MultiFieldPanel(
        #                     [
        #                         FieldPanel("portfolio_cta_primary_text"),
        #                         PageChooserPanel("portfolio_cta_primary_link"),
        #                     ],
        #                     heading="Primary Button",
        #                 ),
        #                 MultiFieldPanel(
        #                     [
        #                         FieldPanel("portfolio_cta_secondary_text"),
        #                         PageChooserPanel("portfolio_cta_secondary_link"),
        #                     ],
        #                     heading="Secondary Button",
        #                 ),
        #             ],
        #             heading="Portfolio CTA Section",
        #             classname="collapsible collapsed",
        #         ),
        #     ],
        #     heading="Portfolio Section",
        # ),
        PageChooserPanel("featured_why_us_section", "services.WhyUsPage"),
    ]

    def primary_cta_link(self):
        if self.hero_primary_cta_page:
            try:
                return self.hero_primary_cta_page.url
            except Exception:
                return None
        if self.hero_primary_cta_url:
            return self.hero_primary_cta_url
        return "#"

    def featured_portfolio(self):
        return self.portfolio_projects.all()

    def featured_portfolio_categories(self):
        """Return distinct PortfolioCategory instances that are used by the
        featured portfolio projects for this homepage.
        """
        try:
            from portfolio.models import PortfolioCategory

            return PortfolioCategory.objects.filter(
                portfoliopage__in=self.portfolio_projects.all()
            ).distinct()
        except Exception:
            return (
                PortfolioCategory.objects.none()
                if "PortfolioCategory" in globals()
                else []
            )

    def portfolio_cta_link(self):
        if self.portfolio_cta_page:
            try:
                return self.portfolio_cta_page.url
            except Exception:
                return None
        if self.portfolio_cta_url:
            return self.portfolio_cta_url
        return "#"
