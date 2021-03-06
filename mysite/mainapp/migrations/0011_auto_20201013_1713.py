# Generated by Django 3.1.1 on 2020-10-13 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_viewing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='like',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='viewing',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='viewing',
            name='object_id',
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(related_name='article_likes', to='mainapp.Like'),
        ),
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.ManyToManyField(related_name='article_views', to='mainapp.Like'),
        ),
    ]
