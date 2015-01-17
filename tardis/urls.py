from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import IndexView, registration, login, logout

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
)