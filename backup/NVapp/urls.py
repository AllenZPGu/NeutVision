from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^score/$', views.score, name='score'),
    url(r'^score/ajax/submit_score/$', views.submit_score, name='submit_score'),
    url(r'^history/$', views.history, name='history'),
    url(r'^examples/$', views.examples, name='examples'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
