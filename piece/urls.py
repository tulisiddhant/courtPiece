from django.conf.urls import url
from piece import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getRoomIds, name='getRoomIds'),
    url(r'^joinRoom/$', views.joinRoom, name='joinRoom'),
    url(r'^newRoom/$', views.newRoom, name='newRoom'),
    url(r'^getGameStatus/$', views.getGameStatus, name='getGameStatus'),
    url(r'^selectPosition/$', views.selectPosition, name='selectPosition'),
    url(r'^setTrump/$', views.setTrump, name='setTrump'),
    url(r'^throwCard/$', views.throwCard, name='throwCard'),
    url(r'^resetState/$', views.resetState, name='resetState'),
    url(r'^newMessage/$', views.newMessage, name='newMessage'),
]
