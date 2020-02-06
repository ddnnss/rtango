from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Item
from django.urls import reverse

class LatestPostsFeed(Feed):
    title = "My blog"
    link = ""
    description = "New posts of my blog."

    def items(self):
        return Item.objects.all()

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return truncatewords(item.description, 30)


    def item_link(self, item):
        return f'/category/{item.category.first().name_slug}/{item.name_slug}/'
