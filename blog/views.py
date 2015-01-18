# -*- coding: utf-8 -*-

import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib import auth
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from blog.models import Category, Post, User
from blog.forms import RegistrationForm, LoginForm


class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class JSONResponseMixin(object):

    def render_to_json_response(self, context, user, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context, user), safe=False,
            **response_kwargs
        )

    def get_data(self, context, user):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        items = context['posts']
        posts = [{
            'id': item.id,
            'title': item.title,
            'text': item.text,
            'author_name': item.author.username,
            'author_url': reverse('author', args=(item.author.id,)),
            'edit_url': reverse('edit_post', args=(item.id,)),
            'edit_flag': user == item.author or user.is_superuser,
            'categories': [{'url': reverse('category', args=(category.id,)), 'name': category.name}
                           for category in item.categories.all()],
            'created': item.created.strftime('%Y-%m-%d %H:%M:%S'),

        } for item in items]
        data = {
            'posts': posts,
            'load_flag': context['load_flag'],
        }
        return data


class AJAXLoadListView(JSONResponseMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super(AJAXLoadListView, self).get_context_data(**kwargs)
        context['load_flag'] = self.load_flag
        context['index_flag'] = kwargs.get('index_flag')
        context['ajax_data'] = json.dumps({
            'category': kwargs.get('category'),
            'author': kwargs.get('author'),
            'query': kwargs.get('query'),
            'load_url': kwargs.get('load_url'),
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return self.render_to_json_response(context, self.request.user)
        else:
            return super(AJAXLoadListView, self).render_to_response(context, **response_kwargs)


class IndexView(AJAXLoadListView):
    template_name = 'main.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-created')[:3]

    def get_queryset(self):
        offset = int(self.request.GET.get('offset', 0))
        qs = Post.objects.all().order_by('-created')
        self.load_flag = True if qs.count() > (offset + settings.POSTS_ON_PAGE) else False
        return qs[offset:offset+settings.POSTS_ON_PAGE]

    def get_context_data(self, **kwargs):
        data = {
            'index_flag': True,
            'load_url': reverse('index'),
        }
        return super(IndexView, self).get_context_data(**data)


class CategoryView(AJAXLoadListView):
    template_name = 'category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        offset = int(self.request.GET.get('offset', 0))
        self.category = get_object_or_404(Category, id=self.args[0])
        qs = Post.objects.filter(categories=self.category.id).order_by('-created')
        self.load_flag = True if qs.count() > (offset + settings.POSTS_ON_PAGE) else False
        return qs[offset:offset+settings.POSTS_ON_PAGE]

    def get_context_data(self, **kwargs):
        data = {
            'load_url': reverse('category', args=(self.category.id,)),
            'category': self.category.id,
        }
        context = super(CategoryView, self).get_context_data(**data)
        context['category'] = self.category.name
        return context


class AuthorView(AJAXLoadListView):
    template_name = 'author.html'
    context_object_name = 'posts'

    def get_queryset(self):
        offset = int(self.request.GET.get('offset', 0))
        self.author = get_object_or_404(User, id=self.args[0])
        qs = Post.objects.filter(author=self.author.id).order_by('-created')
        self.load_flag = True if qs.count() > (offset + settings.POSTS_ON_PAGE) else False
        return qs[offset:offset+settings.POSTS_ON_PAGE]

    def get_context_data(self, **kwargs):
        data = {
            'load_url': reverse('author', args=(self.author.id,)),
            'author': self.author.id,
        }
        context = super(AuthorView, self).get_context_data(**data)
        context['author'] = self.author.username
        return context


class SearchView(AJAXLoadListView):
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        offset = int(self.request.GET.get('offset', 0))
        self.query = self.request.GET.get('q')
        qs = []
        if self.query:
            query = self.query.strip().split(' ')
            if query:
                query_list = [(Q(text__contains=word) | Q(title__contains=word) |
                    Q(categories__name__contains=word)) for word in query]
                query = reduce(lambda a, b: a & b, query_list)
                qs = Post.objects.filter(query).distinct().order_by('-created')
        else:
            self.query = ''

        self.load_flag = True if (qs and qs.count()) > (offset + settings.POSTS_ON_PAGE) else False
        return qs[offset:offset+settings.POSTS_ON_PAGE]

    def get_context_data(self, **kwargs):
        data = {
            'load_url': reverse('basic_search')+'?q=%s' % self.query,
            'query': self.query,
        }
        context = super(SearchView, self).get_context_data(**data)
        context['query'] = self.query
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text', 'categories']
    template_name = 'post_form.html'

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'categories']
    template_name = 'post_form.html'

    def get_success_url(self):
        return reverse('index')

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_superuser or context['post'].author == self.request.user:
            return super(PostEditView, self).render_to_response(context, **response_kwargs)
        else:
            return render(self.request, 'access_error.html', {})


def registration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'], password=data['password1'])
            user.save()
            user_to_auth = auth.authenticate(username=data['username'], password=data['password1'])
            auth.login(request, user_to_auth)

            return HttpResponseRedirect(reverse('index'))

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))