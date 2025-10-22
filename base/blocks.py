from django.utils.functional import cached_property
from wagtail.blocks import (
    StreamBlock,
    StructBlock,
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    ListBlock,
    PageChooserBlock,
    TextBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images import get_image_model


class ImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)

    @cached_property
    def preview_image(self):
        # Cache the image object for previews to avoid repeated queries
        return get_image_model().objects.last()

    def get_preview_value(self):
        return {
            **self.meta.preview_value,
            "image": self.preview_image,
            "caption": self.preview_image.description,
        }

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"
        preview_value = {"attribution": "Sigmora"}
        description = "An image with optional caption"


class HeadingBlock(StructBlock):
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Select a header size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"
        preview_value = {"heading_text": "Forex App Types", "size": "h2"}
        description = "A heading with level two, three, or four"


class AccordionBlock(StructBlock):
    """An accordion block with a title and rich text content."""

    title = CharBlock(required=True, help_text="Add the title for the accordion item")
    content = RichTextBlock(
        required=True, help_text="Add the content for the accordion item"
    )

    class Meta:
        template = "blocks/accordion_block.html"
        icon = "arrow-down"
        label = "Accordion"


class FeatureBlock(StructBlock):
    """A block for listing key features."""

    title = CharBlock(
        required=True, help_text="Add a title for the feature list (e.g., Key Features)"
    )
    features = ListBlock(CharBlock(label="Feature"))

    class Meta:
        template = "blocks/feature_block.html"
        icon = "star"
        label = "Feature List"


class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph_block.html",
        description="A rich text paragraph",
    )

    image_block = ImageBlock()
    accordion = AccordionBlock()
    feature_list = FeatureBlock()


class LinkBlock(StructBlock):
    """A block for a single link, with text and a page chooser."""

    link_text = CharBlock(required=True, max_length=100)
    link_page = PageChooserBlock(required=True)

    class Meta:
        icon = "link"
        label = "Page Link"


class LinkColumnBlock(StructBlock):
    """A block for a whole column of links in the footer."""

    title = CharBlock(required=True, max_length=100)
    links = ListBlock(LinkBlock())

    class Meta:
        icon = "list-ul"
        label = "Link Column"


class ImageWithCaptionBlock(StructBlock):
    """A custom block for an image with an optional caption."""

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False, help_text="Add a caption for the image.")

    class Meta:
        icon = "image"
        label = "Image with Caption"
        template = "blocks/image_with_caption_block.html"


class QuoteBlock(StructBlock):
    """A custom block for a pull quote with an author."""

    quote_text = TextBlock(required=True, rows=3)
    author = CharBlock(required=False, max_length=100)

    class Meta:
        icon = "openquote"
        label = "Quote"
