from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet

from portfolio.blocks import PortfolioStreamBlock


@register_snippet
class PortfolioCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text=_('A slug to identify posts by this category'),
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = _("Portfolio Category")
        verbose_name_plural = _("Portfolio Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name

class PortfolioPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'portfolio.PortfolioPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class PortfolioPage(Page):
    client = models.CharField(max_length=255, blank=True)
    project_date = models.DateField("Project date", blank=True, null=True)
    project_website = models.URLField(blank=True)
    lead_paragraph = RichTextField(blank=True)
    
    body = StreamField(PortfolioStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True)

    tags = ClusterTaggableManager(through=PortfolioPageTag, blank=True, verbose_name=_('Tech Stack'))
    categories = ParentalManyToManyField('portfolio.PortfolioCategory', blank=True)

    live_project_url = models.URLField(blank=True, help_text=_("The URL to the live project"))
    next_project_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Select the next project to display"),
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('client'),
            FieldPanel('project_date'),
            FieldPanel('project_website'),
        ], heading=_("Project Meta")),
        FieldPanel('lead_paragraph'),
        InlinePanel('gallery_images', label=_("Gallery images")),
        FieldPanel('tags'),
        FieldPanel('categories'),
        FieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('live_project_url'),
            FieldPanel('next_project_page'),
        ], heading=_("Project Links")),
    ]

    class Meta:
        verbose_name = _("Portfolio Page")

class PortfolioPageGalleryImage(Orderable):
    page = ParentalKey(PortfolioPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]