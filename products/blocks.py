from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, ListBlock


# Accordion block: a list of accordion items (title, icon, body)
class AccordionItem(StructBlock):
    title = CharBlock(required=True)
    icon = CharBlock(required=False, help_text="Icon CSS class, e.g. 'bi bi-clipboard-data'", blank=True)
    body = RichTextBlock(required=True)

    class Meta:
        template = "products/blocks/accordion_item.html"


class AccordionBlock(StructBlock):
    items = ListBlock(AccordionItem())

    class Meta:
        icon = "list-ul"
        template = "products/blocks/accordion_block.html"

