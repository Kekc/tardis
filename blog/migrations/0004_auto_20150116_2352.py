# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_entry_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Blog post title')),
                ('text', models.TextField(verbose_name='Blog post text')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('edited', models.DateTimeField(auto_now=True, verbose_name='Edited at')),
                ('author', models.ForeignKey(verbose_name='Author', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='blog.Category', null=True, verbose_name='Categories', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='entry',
            name='author',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='categories',
        ),
        migrations.DeleteModel(
            name='Entry',
        ),
    ]
