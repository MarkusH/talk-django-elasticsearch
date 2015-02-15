from elasticsearch_dsl import DocType, String, Date, Boolean


class Article(DocType):
    author = String(analyzer='snowball')
    title = String(analyzer='snowball', boost=5,
                   fields={'raw': String(index='not_analyzed')})
    slug = String(index='no')
    text = String(analyzer='snowball',
                  fields={'raw': String(index='not_analyzed')})
    publish_datetime = Date()
    is_public = Boolean()
    category = String(analyzer='snowball',
                      fields={'raw': String(index='not_analyzed')})

    url = String(index='no')
    category_url = String(index='no')

    class Meta:
        index = 'blog'

    def __str__(self):
        return self.title


def init():
    Article.init()
