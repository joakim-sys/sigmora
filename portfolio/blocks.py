from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    ListBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "portfolio/blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """

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
        template = "portfolio/blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """

    text = TextBlock()
    attribute_name = CharBlock(blank=True, required=False, label="e.g. Mary Berry")

    class Meta:
        icon = "openquote"
        template = "portfolio/blocks/blockquote.html"

# Accordion block: a list of accordion items (title, icon, body)
class AccordionItem(StructBlock):
    title = CharBlock(required=True)
    icon = CharBlock(required=False, help_text="Icon CSS class, e.g. 'bi bi-clipboard-data'", blank=True)
    body = RichTextBlock(required=True)

    class Meta:
        template = "portfolio/blocks/accordion_item.html"


class AccordionBlock(StructBlock):
    items = ListBlock(AccordionItem())

    class Meta:
        icon = "list-ul"
        template = "portfolio/blocks/accordion_block.html"


# Feature list block: title + list of feature items (text + optional icon)
class FeatureItem(StructBlock):
    text = CharBlock(required=True)
    icon = CharBlock(required=False, blank=True, help_text="Icon CSS class, e.g. 'bi bi-check2-circle'")

    class Meta:
        template = "portfolio/blocks/feature_item.html"


class FeatureListBlock(StructBlock):
    title = CharBlock(required=False, blank=True)
    features = ListBlock(FeatureItem())

    class Meta:
        icon = "list-ul"
        template = "portfolio/blocks/feature_list_block.html"


class SpacerBlock(StructBlock):
    size = ChoiceBlock(
        choices=[
            ("xs", "Extra small (8px)"),
            ("sm", "Small (16px)"),
            ("md", "Medium (32px)"),
            ("lg", "Large (48px)"),
            ("xl", "Extra large (64px)"),
        ],
        default="md",
        help_text="Choose spacing size",
    )

    class Meta:
        icon = "placeholder"
        template = "portfolio/blocks/spacer_block.html"


class PortfolioStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="pilcrow", template="portfolio/blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text="Insert an embed from URL",
        icon="media",
        template = "portfolio/blocks/embed_block.html",
    )

    accordion = AccordionBlock()
    feature_list = FeatureListBlock()
    spacer = SpacerBlock()
    # Removed nested classes AccordionItem, AccordionBlock, FeatureItem, FeatureListBlock