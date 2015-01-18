from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import IndexView, RegistrationView, LoginView, LogoutView, CategoryView, AuthorView, PostCreateView, PostEditView, \
    PostDeleteView, SearchView

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^search/', include('haystack.urls')),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^category/(?P<pk>\d+)/$', CategoryView.as_view(), name='category'),
    url(r'^author/(?P<pk>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^basic_search/$', SearchView.as_view(), name='basic_search'),

    url(r'post/add/$', PostCreateView.as_view(), name='add_post'),
    url(r'post/edit/(?P<pk>\d+)/$', PostEditView.as_view(), name='edit_post'),
    url(r'post/delete/(?P<pk>\d+)/$', PostDeleteView.as_view(), name='delete_post'),
)