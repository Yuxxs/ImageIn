from django import forms

import django_filters
from mainapp.models import Article

from mainapp.models import HashTag


class ArticleFilter(django_filters.FilterSet):
    choices = HashTag.objects.all()
    choices.query.set_limits(0, 100)
    tag = django_filters.ChoiceFilter(label='Фильтр по хештегу', method='filterbyhashtag',choices=[
    (choice, choice) for choice in choices])

    def filterbyhashtag(self, queryset, value, *args, **kwargs):
        tag = HashTag.objects.filter(name=args[0])
        #articles = tag.article
        queryset = Article.objects.filter(hashtag__name=args[0])
        return queryset

    class Meta:
        model = Article
        fields = ()
