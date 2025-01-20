from django import template
from django.contrib.auth import get_user_model
from django.utils.html import format_html

register = template.Library()
user_model = get_user_model()

@register.filter
def author_details(author, user=None):
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""

    if author == user:
      return format_html('<strong>me</strong>')

    name = f"{author.first_name} {author.last_name}" if author.first_name and author.last_name else author.username

    return format_html('<a href="mailto:{}">{}</a>', author.email, name) if author.email else name