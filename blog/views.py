# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from blog.models import Category


class CategoryListView(ListView):
    model = Category
    template_name = 'main.html'
    context_object_name = 'categories'

