from .search import Article


def post_save_article(sender, instance, created, **kwargs):
    if created:
        article = Article(id=instance.pk)
    else:
        article = Article.get(id=instance.pk)
    data = {
        'author': instance.author.get_full_name() or instance.author.username,
        'title': instance.title,
        'slug': instance.slug,
        'text': instance.text,
        'publish_datetime': instance.publish_datetime,
        'is_public': instance.is_public,
        'category': instance.category.title,
        'url': instance.get_absolute_url(),
        'category_url': instance.category.get_absolute_url(),
    }
    for k, v in data.items():
        setattr(article, k, v)
    article.save()


def post_delete_article(sender, instance, **kwargs):
    article = Article.get(id=instance.pk)
    article.delete()
