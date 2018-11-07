from django.urls import re_path
from blog.views import RSSFeed
from . import views


app_name = 'blog'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^page/(?P<page>[0-9]+)/$', views.get_page, name='page'),
    re_path(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    re_path(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    re_path(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    re_path(r'^tag/(?P<pk>[0-9]+)/$', views.tag, name='tag'),
    re_path(r'^rss/$', RSSFeed, name="RSS"),

]