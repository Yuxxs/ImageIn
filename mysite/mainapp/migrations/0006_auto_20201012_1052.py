# Generated by Django 3.1.1 on 2020-10-12 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20201011_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='post',
        ),
        migrations.AddField(
            model_name='article',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]