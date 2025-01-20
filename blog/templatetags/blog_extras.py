from django import template
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from blog.models import Post

register = template.Library()
user_model = get_user_model()

@register.filter
def author_details(author, user=None):
  return author_name(author, user)


@register.simple_tag(takes_context=True)
def author_details_tag(context):
  request = context["request"]
  user = request.user
  post = context["post"]
  author = post.author

  return author_name(author, user)
    

def author_name(author, user=None):
  if not isinstance(author, user_model):
    return ""

  if author == user:
    return format_html('<strong>me</strong>')

  name = f"{author.first_name} {author.last_name}" if author.first_name and author.last_name else author.username

  return format_html('<a href="mailto:{}">{}</a>', author.email, name) if author.email else name


@register.simple_tag
def row(extra_classes=""):
  return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
  return format_html("</div>")


@register.simple_tag
def col(extra_classes=""):
  return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
  return format_html("</div>")


@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    return {"title": "Recent Posts", "posts": posts}