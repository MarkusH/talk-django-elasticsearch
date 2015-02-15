from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, db_index=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:category-detail", kwargs={'slug': self.slug})


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, db_index=True)
    text = models.TextField()
    publish_datetime = models.DateTimeField()
    is_public = models.BooleanField(default=False)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:article-detail", kwargs={'slug': self.slug})
