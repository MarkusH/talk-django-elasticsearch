from celery import shared_task
from elasticsearch import NotFoundError

from .search import Article as SearchArticle


@shared_task(bind=True, default_retry_delay=60, max_retries=3)
def index_article(self, pk):
    from .models import Article
    try:
        article = Article.objects.select_related('author', 'category').get(pk=pk)
    except Article.ObjectDoesNotExist:
        self.retry()

    try:
        search_article = SearchArticle.get(id=pk)
    except NotFoundError:
        search_article = SearchArticle(meta={'id': pk})
    data = {
        'author': article.author.get_full_name() or article.author.username,
        'title': article.title,
        'slug': article.slug,
        'text': article.text,
        'publish_datetime': article.publish_datetime,
        'is_public': article.is_public,
        'category': article.category.title,
        'url': article.get_absolute_url(),
        'category_url': article.category.get_absolute_url(),
    }
    for k, v in data.items():
        setattr(search_article, k, v)
    search_article.save()


@shared_task
def unindex_article(pk):
    try:
        article = SearchArticle.get(id=pk)
    except NotFoundError:
        pass
    else:
        article.delete()
