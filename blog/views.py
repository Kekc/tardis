# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib import auth

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