# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(u'Category', max_length=255)

    class Meta:
        verbose_name_plural = u'Categories'

    def __unicode__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(u'Blog post title', max_length=255)
    text = models.TextField(u'Blog post text')
    author = models.ForeignKey(User, verbose_name=u'Author')
    categories = models.ManyToManyField(Category, blank=True, null=True, verbose_name=u'Categories')
    created = models.DateTimeField(u'Created at', auto_now_add=True)
    edited = models.DateTimeField(u'Edited at', auto_now=True)

    def __unicode__(self):
        return '{0}, {1}'.format(self.author.username, self.created.strftime('%Y-%m-%d %H:%M:%S'))