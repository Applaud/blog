from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from models import Entry

class LatestEntriesRSS(Feed):
    feed_type = Rss201rev2Feed
    link = ''
    
    def items(self):
        return Entry.objects.order_by('-date')[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_link(self, item):
        return 'http://127.0.0.1:8000/entry/%s' % item.normalized_title
    
    def item_description(self, item):
        return '%s...' % item.body[:50]

# class LatestEntriesAtom(LatestEntriesRSS):
#     feed_type = Atom1Feed
#     subtitle = ''
