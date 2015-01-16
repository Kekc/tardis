# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.inclusion_tag('navigation.html', takes_context=True)
def navigation(context):
    request = context['request']
    print request.user
    home_item = {
        'name': 'home',
        'link': 'index',
    }
    signup_item = {
        'name': 'sign up',
        'link': 'index',
    }
    signin_item = {
        'name': 'sign in',
        'link': 'index',
    }
    newpost_item = {
        'name': 'add post',
        'link': 'index',
    }
    items = [home_item]
    if request.user.is_authenticated():
        items.append(newpost_item)
    else:
        items.extend([signup_item, signin_item])
    return {'items': items}