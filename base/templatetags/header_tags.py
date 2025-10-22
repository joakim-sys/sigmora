from django import template
from base.models import Header

register = template.Library()


@register.simple_tag(takes_context=True)
def header_snippet(context):
    """Return the first Header snippet instance or None."""
    try:
        return Header.objects.first()
    except Exception:
        return None
