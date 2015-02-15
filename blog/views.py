from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.views.generic import DetailView, ListView

from .models import Article, Category
from .search import Article as SearchArticle


def index(request):
    return redirect(reverse('blog:article-list'))


class ArticleDetailView(DetailView):
    model = Article

    def get_queryset(self):
        qs = super(ArticleDetailView, self).get_queryset()
        qs = qs.select_related('author', 'category')
        if not self.request.user.is_authenticated():
            qs = qs.filter(is_public=True, publish_datetime__lte=now())
        return qs

article_detail = ArticleDetailView.as_view()


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        qs = super(ArticleListView, self).get_queryset()
        qs = qs.select_related('author', 'category')
        if not self.request.user.is_authenticated():
            qs = qs.filter(is_public=True, publish_datetime__lte=now())
        return qs

article_list = ArticleListView.as_view()


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        ctx = super(CategoryDetailView, self).get_context_data(**kwargs)
        articles = self.object.article_set
        if not self.request.user.is_authenticated():
            articles = articles.filter(
                is_public=True, publish_datetime__lte=now()
            )
        ctx['articles'] = articles.all()
        return ctx

category_detail = CategoryDetailView.as_view()


class CategoryListView(ListView):
    model = Category

category_list = CategoryListView.as_view()


def search(request):
    q = request.GET.get('q', '')
    ctx = {'query': q, 'results': []}
    if q:
        search = SearchArticle.search()
        search = search.query(
            'simple_query_string',
            query=q,
            fields=['title', 'text']
        )
        if not request.user.is_authenticated():
            search = search.filter('term', is_public=True)
            search = search.filter('range', publish_datetime={'lte': 'now'})
        ctx['results'] = search.execute()
    return render(request, 'blog/search.html', ctx)
