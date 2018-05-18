from museum_app import views as vs
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
# from django.views.generic.base import TemplateView
from museum_app.feeds import top_museums_feed, last_comment_feed
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^custom.css$', vs.load_custom_CSS),
    url(r'^signup/?$', vs.sign_up),
    url(r'^login/?$', login),
    url(r'^logout/?$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}),
    url(r'^topmuseums/?$', top_museums_feed()),
    url(r'^lastcomments/?$', last_comment_feed()),
    url(r'^museo/?$', vs.load_museums),
    url(r'^museos/?$', vs.museums),
    url(r'^museos/(?P<ID>\d+)$', vs.museum, name = 'museum'),
    url(r'^(?P<user_name>.+)/xml$', vs.user_xml),
    url(r'^(?P<user_name>.+)$', vs.user),
    url(r'^$', vs.main_page)
]
