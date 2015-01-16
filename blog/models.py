# -*- coding: utf-8 -*-

from django.db import models


class Category(models.Model):
    name = models.CharField(u'Category', max_length=255, db_index=True)

    class Meta:
        verbose_name_plural = u'Categories'

    def __unicode__(self):
        return self.name
