from wagtail.blocks import (
    StructBlock,
    CharBlock,
    IntegerBlock,
    TextBlock,
    ListBlock, 
    URLBlock
)

from wagtail.images.blocks import ImageChooserBlock

# Service blocks

class ImageBlock(ImageChooserBlock):
    """A simple block for choosing an image, with a custom template."""
    class Meta:
        icon = 'image'
        label = 'Full Width Image'
        template = 'services/blocks/image_block.html'

class ImageUrlBlock(StructBlock):
    image_url = URLBlock()
    class Meta:
        icon = 'image'
        label = 'Full Width Image'
        template = 'services/blocks/image_url_block.html'

class FeatureItemBlock(StructBlock):
    """A block for a single feature item with an icon, title, and text."""

    icon_class = CharBlock(
        required=True,
        help_text="The Bootstrap Icon class (e.g., 'bi bi-graph-up-arrow').",
    )
    title = CharBlock(required=True, max_length=100)
    text = TextBlock(required=True)

    class Meta:
        icon = "tick-inverse"
        label = "Feature Item"


class FeatureGridBlock(StructBlock):
    """A block for the entire 'What's Included' grid of features."""

    title = CharBlock(required=True, default="What's Included")
    features = ListBlock(FeatureItemBlock())

    class Meta:
        icon = "grid"
        label = "Features Grid"
        template = "services/blocks/feature_grid_block.html"

class ProcessStepBlock(StructBlock):
    """A block for a single step in the 'Our Process' section."""
    title = CharBlock(required=True, max_length=100)
    text = TextBlock(required=True)

    class Meta:
        icon = 'arrow-right'
        label = 'Process Step'

class ProcessListBlock(StructBlock):
    """A block for the entire 'Our Process' list of steps."""
    title = CharBlock(required=True, default="Our Process")
    steps = ListBlock(ProcessStepBlock())

    class Meta:
        icon = 'list-ol'
        label = 'Process List'
        template = 'services/blocks/process_list_block.html'


#  Why Us Block


class WFeatureCardBlock(StructBlock):
    """A block for the feature cards with an icon, title, text, and stats."""

    icon_class = CharBlock(required=True, help_text="e.g., 'bi bi-palette-fill'")
    title = CharBlock(required=True)
    text = TextBlock(required=True)
    stat_number = IntegerBlock(required=True)
    stat_label = CharBlock(required=True)

    class Meta:
        template = "services/blocks/wfeature_card_block.html"
        icon = "features"
        label = "Feature Card"


class WFeatureItemBlock(StructBlock):
    """A block for the smaller feature items with an icon, title, and text."""

    icon_class = CharBlock(default="bi bi-check-circle-fill", required=True)
    title = CharBlock(required=True)
    text = TextBlock(required=True)

    class Meta:
        template = "services/blocks/wfeature_item_block.html"
        icon = "tick-inverse"
        label = "Feature Item"
