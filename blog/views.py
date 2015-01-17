# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib import auth
from django.db.models import Q

from blog.models import Category, Post, User
from blog.forms import RegistrationForm, LoginForm


class IndexView(ListView):
    template_name = 'main.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-created')[:3]


class CategoryView(ListView):
    template_name = 'category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.args[0])
        return Post.objects.filter(categories=self.category.id).order_by('-created')[:3]

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = self.category.name
        return context


class AuthorView(ListView):
    template_name = 'author.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.author = get_object_or_404(User, id=self.args[0])
        return Post.objects.filter(author=self.author.id).order_by('-created')[:3]

    def get_context_data(self, **kwargs):
        context = super(AuthorView, self).get_context_data(**kwargs)
        context['author'] = self.author.username
        return context


class SearchView(ListView):
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.query = self.request.GET.get('search')
        query = self.query.strip().split(' ')
        print query
        if query:
            query_list = [(Q(text__contains=word) | Q(title__contains=word) |
                Q(categories__name__contains=word)) for word in query]
            query = reduce(lambda a, b: a & b, query_list)
            qs = Post.objects.filter(query).distinct()
            print query
        else:
            qs = Post.objects.all()
        return qs.order_by('-created')[:3]

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['query'] = self.query
        return context


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