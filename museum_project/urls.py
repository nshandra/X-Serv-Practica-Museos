from museum_app import views as vs
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
# from django.views.generic.base import TemplateView
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/?$', vs.sign_up),
    url(r'^login/?$', login),
    url(r'^logout/?$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}),
    url(r'^museo/?$', vs.load_museums),
    url(r'^museos/?$', vs.museums),
    url(r'^museos/(\d+)$', vs.museum),
    url(r'^(.+)$', vs.user),
    url(r'^$', vs.main_page)
]
