from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import CategoryListView

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', CategoryListView.as_view()),
)