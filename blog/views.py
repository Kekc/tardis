# -*- coding: utf-8 -*-

import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib import auth
from django.db.models import Q

from blog.models import Category, Post, User
from blog.forms import RegistrationForm, LoginForm


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
            'categories': [{'url': reverse('category', args=(category.id,)), 'name': category.name} for category in item.categories.all()],

        } for item in items]
        data = {
            'posts': posts,
            'load_flag': context['load_flag'],
        }
        return data


class IndexView(JSONResponseMixin, ListView):
    template_name = 'main.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-created')[:3]

    def get_queryset(self):
        offset = int(self.request.GET.get('offset', 0))
        qs = Post.objects.all().order_by('-created')
        self.load_flag = True if qs[offset+3:offset+4] else False
        return qs[offset:offset+3]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['load_flag'] = self.load_flag
        context['ajax_data'] = json.dumps({
            'category': None,
            'author': None,
            'query': None,
            'load_url': reverse('index'),
        })
        return context

    def render_to_response(self, context):
        if self.request.is_ajax():
            return self.render_to_json_response(context, self.request.user)
        else:
            return super(IndexView, self).render_to_response(context)


class CategoryView(JSONResponseMixin, ListView):
    template_name = 'category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        offset = int(self.request.GET.get('offset', 0))
        self.category = get_object_or_404(Category, id=self.args[0])
        qs = Post.objects.filter(categories=self.category.id).order_by('-created')
        self.load_flag = True if qs[offset+3:offset+4] else False
        return qs[offset:offset+3]

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = self.category.name
        context['load_flag'] = self.load_flag
        context['ajax_data'] = json.dumps({
            'category': self.category.id,
            'author': None,
            'query': None,
            'load_url': reverse('category', args=(self.category.id,)),
        })
        return context

    def render_to_response(self, context):
        if self.request.is_ajax():
            return self.render_to_json_response(context, self.request.user)
        else:
            return super(CategoryView, self).render_to_response(context)


class AuthorView(JSONResponseMixin, ListView):
    template_name = 'author.html'
    context_object_name = 'posts'

    def get_queryset(self):
        offset = int(self.request.GET.get('offset', 0))
        self.author = get_object_or_404(User, id=self.args[0])
        qs = Post.objects.filter(author=self.author.id).order_by('-created')
        self.load_flag = True if qs[offset+3:offset+4] else False
        return qs[offset:offset+3]

    def get_context_data(self, **kwargs):
        context = super(AuthorView, self).get_context_data(**kwargs)
        context['author'] = self.author.username
        context['load_flag'] = self.load_flag
        context['ajax_data'] = json.dumps({
            'category': None,
            'author': self.author.id,
            'query': None,
            'load_url': reverse('author', args=(self.author.id,)),
        })
        return context

    def render_to_response(self, context):
        if self.request.is_ajax():
            return self.render_to_json_response(context, self.request.user)
        else:
            return super(AuthorView, self).render_to_response(context)


class SearchView(JSONResponseMixin, ListView):
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        offset = int(self.request.GET.get('offset', 0))
        self.query = self.request.GET.get('query')

        query = self.query.strip().split(' ')
        if query:
            query_list = [(Q(text__contains=word) | Q(title__contains=word) |
                Q(categories__name__contains=word)) for word in query]
            query = reduce(lambda a, b: a & b, query_list)
            qs = Post.objects.filter(query).distinct().order_by('-created')
        else:
            qs = []

        self.load_flag = True if qs[offset+3:offset+4] else False
        return qs[offset:offset+3]

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['query'] = self.query
        context['load_flag'] = self.load_flag
        context['ajax_data'] = json.dumps({
            'category': None,
            'author': None,
            'query': self.query,
            'load_url': reverse('search')+'?%s' % self.query,
        })
        return context

    def render_to_response(self, context):
        if self.request.is_ajax():
            return self.render_to_json_response(context, self.request.user)
        else:
            return super(SearchView, self).render_to_response(context)


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'text', 'categories']
    template_name = 'post_form.html'

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostEditView(UpdateView):
    model = Post
    fields = ['title', 'text', 'categories']
    template_name = 'post_form.html'

    def get_success_url(self):
        return reverse('index')


def registration(request):
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = auth.authenticate(username=data['username'], password=data['password'])
            auth.login(request, user)

            return HttpResponseRedirect(reverse('index'))

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))