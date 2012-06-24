from django.conf.urls import patterns, include, url
from app import views, feeds
import settings

urlpatterns = patterns('',
                       url(r'^$', views.main_page),
                       url(r'^entry/(?P<title>.*)$', views.entry),
                       url(r'^team/(?P<name>.*)$', views.team),
                       url(r'^beads/$', views.beads),
                       url(r'^photos/$', views.photos),
                       (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.STATIC_ROOT}),
                       (r'^feed/rss$', feeds.LatestEntriesRSS()),
                       (r'^post$', views.post),
                       )
