from django import template
from wagtail.models import Site
from base.models import FooterSettings

register = template.Library()


@register.inclusion_tag("includes/sections/why_us.html")
def render_why_us_section(why_us_page):
    """
    A template tag that takes a WhyUsPage object and renders the
    why_us.html template with that page's context.
    """
    return {
        "page": why_us_page,
    }


# @register.inclusion_tag('includes/footer.html', takes_context=True)
# def footer(context):
#     """
#     An inclusion tag to render the footer.
#     It fetches the FooterSettings for the current site.
#     """
#     return {
#         'settings': FooterSettings.for_site(context['request'].site),
#         'request': context['request'],
#     }


@register.inclusion_tag("includes/footer.html", takes_context=True)
def footer(context):
    """
    An inclusion tag to render the footer.
    It fetches the FooterSettings for the current site.
    """
    # Get the request from the context
    request = context["request"]

    # Manually find the site using the method that works, instead of relying on middleware.
    current_site = Site.find_for_request(request)

    # If a site is found, get the settings for it.
    if current_site:
        return {
            "settings": FooterSettings.for_site(current_site),
            "request": request,
            'current_site': current_site, 
        }

    # Return an empty context if no site is found, to prevent errors.
    return {
        "request": request,
    }
