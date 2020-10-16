from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from mainapp import models

admin.site.register(models.Article)
admin.site.register(models.Like)
admin.site.register(models.Viewing)
admin.site.register(models.HashTag)
