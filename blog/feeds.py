from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class LatestPostsFeed(Feed):
    title = "blog newest posts"
    link = "/blog/rss/feed/"
    description = "New posts of my blog"
    
    def items(self):
        return Post.objects.filter(status=1)
    
    def item_title(self, item):
        return item.title   
    
    def item_description(self, item):
        return item.content[:100]
    
    def item_link(self, item):
        return reverse('blog:single', args=[item.id])
    
   
    
