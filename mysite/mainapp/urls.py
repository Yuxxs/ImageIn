from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import *
from mainapp import views


urlpatterns = [
   path('mainpage/admin/', views.AdminMainPage.as_view(), name='adminpage'),
   path('feed/', views.FeedPage.as_view(), name='feedpage'),
   path('articles/<int:article_id>', views.ArticlePage.as_view(), name='articlepage'),
   path('articles/<int:article_id>/delete', views.ArticlePage.delete, name='articledelete'),
   path('articles/<int:article_id>/edit', views.ArticleEdit.as_view(), name='articleedit'),
   path('articles/<int:article_id>/like', views.ArticlePage.increment_likes, name='articlelike'),

   path('<str:username>/mainpage/', views.UserMainPage.as_view(), name='userpage'),

   path('login/', views.LoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path("register/", views.register, name="register"),

   path('adminuserdelete/<str:username>', views.AdminMainPage.delete, name='adminuserdelete'),
   path('adminuserunblock/<str:username>', views.AdminMainPage.unblock, name='adminuserunblock'),
   path('adminuserblock/<str:username>', views.AdminMainPage.block, name='adminuserblock'),
]
