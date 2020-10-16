import datetime

from django.db import models

# Create your models here

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AbstractUser, User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
import settings
from importlib_resources._common import _


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)


class Viewing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='views',
                             on_delete=models.CASCADE)


class Article(models.Model):
    postdate = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(default='', null=True, max_length=50)
    description = models.TextField(default='', null=True)
    image = models.ImageField(upload_to='upload/')
    likes = models.ManyToManyField(Like, symmetrical=False,related_name='article_likes')
    views = models.ManyToManyField(Viewing, symmetrical=False,related_name='article_views')

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_views(self):
        return self.views.count()


class HashTag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    article = models.ManyToManyField(Article,related_name='hashtag')

    def __str__(self):
        return self.name
