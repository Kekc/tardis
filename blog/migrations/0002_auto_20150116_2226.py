# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='Blog entry text')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('edited', models.DateTimeField(auto_now=True, verbose_name='Edited at')),
                ('author', models.ForeignKey(verbose_name='Author', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='blog.Category', null=True, verbose_name='Categories', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Entries',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Category'),
            preserve_default=True,
        ),
    ]
