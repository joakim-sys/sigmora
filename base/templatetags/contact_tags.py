from django import template
from contact.models import ContactPage

register = template.Library()

@register.inclusion_tag('includes/sections/contact.html', takes_context=True)
def contact_section(context):
    # Get the first ContactPage instance
    contact_page = ContactPage.objects.live().first()
    
    if contact_page:
        # If a ContactPage exists, get its form
        form = contact_page.get_form(page=contact_page)
        return {
            'page': contact_page,
            'form': form,
            'request': context.get('request'),
        }
    
    # If no ContactPage exists, return an empty context
    return {}
