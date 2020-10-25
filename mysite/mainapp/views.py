from tempfile import NamedTemporaryFile
from urllib.parse import urlparse

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, redirect
import datetime
# Create your views here.
from django.template.context_processors import csrf
from django.template.defaulttags import register
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

import mainapp
from mainapp.models import Article, HashTag, Like, Viewing

from django.contrib.auth import *

from django.views.generic import View
from django.urls import reverse

from mainapp.forms import ArticleForm, HashTagForm, CustomUserCreationForm

import urllib
from django.core.files import File
import urllib.request


@permission_classes((permissions.AllowAny,))
class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration/login.html'

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('userpage',
                                        kwargs={"username": request.user.username}))
            else:
                return redirect('login')
        else:
            return redirect('login')

    def get(self, request):
        form = AuthenticationForm()
        return Response({'form': form})


@permission_classes((permissions.AllowAny,))
class UserMainPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_mainpage.html'

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            img_url = form.cleaned_data["url"]
            note = form.save(commit=False)
            note.author = request.user
            if img_url:
                """
                content = urllib.request.urlretrieve(img_url,
                                                     str(settings.MEDIA_ROOT) +"/"+ Article.generate_upload_path(self=None,
                                                                                                     filename="img.jpg"))
                """
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urllib.request.urlopen(img_url).read())
                img_temp.flush()
                note.image = File(img_temp)

            note.save()
        return redirect(reverse('userpage',
                                kwargs={"username": request.user.username}))

    def get(self, request, *args, **kwargs):
        articleform = ArticleForm()
        hashtagform = HashTagForm(request.GET)
        if hashtagform.is_valid():
            tag = hashtagform.cleaned_data["name"]
            if tag:
                articles = Article.objects.filter(author=request.user, hashtag__name=tag)
            else:
                articles = Article.objects.filter(author=request.user)
        else:
            articles = Article.objects.filter(author=request.user)
        return Response({'hashtagform': hashtagform, 'articleform': articleform, 'articles': articles})


@permission_classes((permissions.AllowAny,))
class FeedPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'feed.html'

    def get(self, request, *args, **kwargs):
        form = HashTagForm(request.GET)
        return Response({'hashtagform': form})

    def load(request, *args, **kwargs):

        num = int(request.GET['num'])
        tag = request.GET['tag']
        if tag:
            articles = Article.objects.order_by('id').filter(hashtag__name=tag)
        else:
            articles = Article.objects.order_by('id').all()
        articles.query.set_limits(num, num + 1)
        html = render_to_string('scroll.html', {'article': articles[0]})
        return HttpResponse(html)


@permission_classes((permissions.AllowAny,))
class ArticlePage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'article.html'

    def delete(request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        article = Article.objects.get(id=article_id)

        article.delete()
        return redirect(reverse('userpage',
                                kwargs={"username": request.user.username}))

    def get(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        article = Article.objects.get(id=article_id)
        hashtags = HashTag.objects.filter(article__id=article_id)
        if not article.author == request.user:
            if len(Article.objects.get(id=article_id).views.filter(user=request.user)) == 0:
                view = Viewing(user=request.user)
                view.save()
                Article.objects.get(id=article_id).views.add(view)
        return Response({'hashtags': hashtags, 'article': article})

    def increment_likes(request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        article = Article.objects.get(id=article_id)
        if not article.author == request.user:
            if len(Article.objects.get(id=article_id).likes.filter(user=request.user)) == 0:
                like = Like(user=request.user)
                like.save()
                article.likes.add(like)
        return redirect(reverse('articlepage',
                                kwargs={"article_id": article_id}))


@permission_classes((permissions.AllowAny,))
class ArticleEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'article_edit.html'

    def post(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        article = Article.objects.get(id=article_id)
        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            form.save()
        return redirect(reverse('articlepage',
                                kwargs={"article_id": article_id}))

    def get(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        article = Article.objects.get(id=article_id)
        articleform = ArticleForm(instance=article)
        hashtagform = HashTagForm()
        hashtags = HashTag.objects.filter(article__id=article_id)
        return Response(
            {'hashtags': hashtags, 'hashtagform': hashtagform, 'articleform': articleform, 'article': article})

    def addhashtag(request, *args, **kwargs):
        form = HashTagForm(request.POST)
        if form.is_valid():
            article_id = kwargs.get('article_id')
            article = Article.objects.get(id=article_id)
            name = form.cleaned_data['name']
            tag = HashTag.objects.filter(name=name)[0]
            if not tag:
                HashTag.objects.create(name=name)
                tag = HashTag.objects.get(name=name)
            if not tag.article.filter(id=article_id):
                tag.article.add(article)
        return redirect(reverse('articleedit',
                                kwargs={"article_id": article_id}))


@permission_classes((permissions.AllowAny,))
class AdminMainPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_admin_mainpage.html'

    def get(request, *args, **kwargs):
        users_list = User.objects.all()
        for i in range(len(users_list)):
            users_list[i].is_active = not users_list[i].is_active
        form = CustomUserCreationForm()
        return Response({'users': users_list, 'form': form})

    def post(request, *args, **kwargs):
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('login')
        return redirect('adminpage')

    def delete(request, *args, **kwargs):

        username = kwargs.get('username')
        User.objects.filter(username=username).delete()
        return redirect('adminpage')

    def block(request, *args, **kwargs):
        username = kwargs.get('username')
        User.objects.filter(username=username).update(is_active=False)
        return redirect('adminpage')

    def unblock(request, *args, **kwargs):
        username = kwargs.get('username')
        User.objects.filter(username=username).update(is_active=True)
        return redirect('adminpage')


def register(request):
    if request.method == "POST":

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            form.save()
        else:
            print(form.errors)
        return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})
