from django import template
from blog.models import (
    BlogCategory,
    BlogPost,
)

register = template.Library()


# ===== Simple Tag =====
@register.simple_tag
def get_blog_categories():
    return BlogCategory.objects.filter(is_active=True)

@register.simple_tag
def get_popular_blog_posts():
    return BlogPost.objects.filter(is_active=True).order_by("-view_count")[:6]
# ===== END Simple Tag =====
