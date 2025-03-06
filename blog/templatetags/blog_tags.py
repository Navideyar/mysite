from django import template
from blog.models import Post
register = template.Library()

@register.simple_tag(name='totalposts')
def total_posts():
    posts = Post.objects.filter(status=1).count()
    return posts

@register.simple_tag (name = 'posts')
def function():
    posts = Post.objects.filter(status=1)
    return  posts

@register.filter(name='snippet')
def snippet(value, arg):
    return value[:arg]  + '...'

@register.inclusion_tag('blog/blog-popular-post.html')
def latestpost(arg=3):
    posts = Post.objects.filter(status=1).order_by('-published_date')[:arg]
    return {'posts': posts}