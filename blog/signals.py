from . import tasks


def post_save_article(sender, instance, **kwargs):
    tasks.index_article.delay(instance.pk)


def post_delete_article(sender, instance, **kwargs):
    tasks.unindex_article.delay(instance.pk)
