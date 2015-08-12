from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.utils.translation import ugettext_lazy as _
from elasticsearch_dsl.connections import connections

from .search import init as init_search
from .signals import post_delete_article, post_save_article


def connect_signals(app):
    Article = app.get_model('article')

    post_save.connect(post_save_article, sender=Article,
                      dispatch_uid='blog.post_save_article')
    post_delete.connect(post_delete_article, sender=Article,
                        dispatch_uid='blog.post_delete_article')


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = _('Blog')

    def ready(self):
        connections.create_connection(**settings.ELASTICSEARCH_CONNS)
        init_search()
        connect_signals(self)
