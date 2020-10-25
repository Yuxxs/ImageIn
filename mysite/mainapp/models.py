import datetime
import os

from django.db import models

# Create your models here

from django.utils import timezone
import settings
from django.utils.text import slugify

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)


class Viewing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='views',
                             on_delete=models.CASCADE)


ARTICLE_UPLOAD_PATH = "upload/articles/"


class Article(models.Model):
    def generate_upload_path(self, filename):
        filename, ext = os.path.splitext(filename.lower())
        filename = "%s.%s%s" % (slugify(filename), datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S"), ext)
        return '%s/%s' % (ARTICLE_UPLOAD_PATH, filename)

    postdate = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(default='', null=True, max_length=50)
    description = models.TextField(default='', null=True)
    image = models.ImageField(blank=True,upload_to=generate_upload_path)
    likes = models.ManyToManyField(Like, symmetrical=False, related_name='article_likes')
    views = models.ManyToManyField(Viewing, symmetrical=False, related_name='article_views')

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_views(self):
        return self.views.count()


class HashTag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    article = models.ManyToManyField(Article, related_name='hashtag')

    def __str__(self):
        return self.name
