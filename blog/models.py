from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField('Category', max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('Blog post title', max_length=255)
    text = models.TextField('Blog post text')
    author = models.ForeignKey(User, verbose_name='Author')
    categories = models.ManyToManyField(Category, blank=True, null=True, verbose_name='Categories')
    created = models.DateTimeField('Created at', auto_now_add=True)
    edited = models.DateTimeField('Edited at', auto_now=True)

    class Meta:
        ordering = ('-created', )

    def __unicode__(self):
        return '{0}, {1}'.format(self.author.username, self.title)