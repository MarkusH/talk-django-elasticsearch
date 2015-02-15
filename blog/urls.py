from django.conf.urls import url

from .views import (
    article_detail, article_list, category_detail, category_list, index, search,
)


urlpatterns = [
    url(r'^article/$', article_list, name='article-list'),
    url(r'^article/(?P<slug>[^/]+)/$', article_detail, name='article-detail'),
    url(r'^category/$', category_list, name='category-list'),
    url(r'^category/(?P<slug>[^/]+)/$', category_detail, name='category-detail'),
    url(r'^search/$', search, name='search'),
    url(r'^$', index, name='index'),
]
