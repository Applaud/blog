from django.conf.urls import patterns, include, url
from app import views, feeds
import settings

urlpatterns = patterns('',
                       url(r'^$', views.main_page),
#                       url(r'^about$', views.about),
                       url(r'^entry/(?P<title>.*)$', views.entry),
                       (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.STATIC_ROOT}),
                       (r'^feed/rss$', feeds.LatestEntriesRSS()),
#                       (r'^feed/atom$', feeds.LatestEntriesAtom()),
                       (r'^post$', views.post),
                       )
