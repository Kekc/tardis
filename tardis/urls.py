from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import IndexView, registration, login, logout, CategoryView, AuthorView, PostCreateView, PostEditView

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^category/(\d+)/$', CategoryView.as_view(), name='category'),
    url(r'^author/(\d+)/$', AuthorView.as_view(), name='author'),

    url(r'post/add/$', PostCreateView.as_view(), name='add_post'),
    url(r'post/edit/(?P<pk>\d+)/$', PostEditView.as_view(), name='edit_post'),
)