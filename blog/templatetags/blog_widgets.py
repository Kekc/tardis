# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django import template

from blog.models import Post

register = template.Library()


@register.inclusion_tag('navigation.html', takes_context=True)
def navigation(context):
    request = context['request']
    data = {}
    home_item = {
        'name': 'home',
        'link': reverse('index'),
    }
    signup_item = {
        'name': 'sign up',
        'link': reverse('registration'),
    }
    signin_item = {
        'name': 'sign in',
        'link': reverse('login'),
    }
    newpost_item = {
        'name': 'add post',
        'link': reverse('add_post'),
    }
    items = [home_item]
    if request.user.is_authenticated():
        items.append(newpost_item)
        data['user'] = request.user.username
    else:
        items.extend([signup_item, signin_item])
    data['items'] = items
    return data

@register.inclusion_tag('post.html', takes_context=True)
def post_template(context, post_id):
    request = context['request']
    data = {}
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        post = None
    edit_flag = request.user == post.author or request.user.is_superuser
    return {'post': post, 'edit_flag': edit_flag}