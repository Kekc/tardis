from django.core.urlresolvers import reverse
from django.conf import settings
from django import template

from blog.models import Post


register = template.Library()


@register.inclusion_tag('navigation.html', takes_context=True)
def navigation(context):
    request = context['request']
    data = {}
    home_item = {
        'name': 'Home',
        'link': reverse('index'),
    }
    signup_item = {
        'name': 'Sign up',
        'link': reverse('registration'),
    }
    signin_item = {
        'name': 'Sign in',
        'link': reverse('login'),
    }
    newpost_item = {
        'name': 'Add post',
        'link': reverse('add_post'),
    }
    items = [home_item]
    if request.user.is_authenticated():
        items.append(newpost_item)
        data['user'] = request.user
    else:
        items.extend([signup_item, signin_item])
    data['items'] = items
    data['search_url'] = reverse(settings.SEARCH_ENGINE)
    data['query'] = context.get('query', '')
    return data

@register.inclusion_tag('post.html', takes_context=True)
def post_template(context, post_id):
    request = context['request']
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        post = None
    if post:
        edit_flag = request.user == post.author or request.user.is_superuser
        return {'post': post, 'edit_flag': edit_flag}
    else:
        return {}