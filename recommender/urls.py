from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$',views.index,name='index'),
    url(r'^recommend/$',views.recommend,name='recommend'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.delete, name='delete'),
    url(r'^rating1/(?P<pk>[0-9]+)/$', views.rating1, name='rating1'),
    url(r'^rating2/(?P<pk>[0-9]+)/$', views.rating2, name='rating2'),
    url(r'^rating3/(?P<pk>[0-9]+)/$', views.rating3, name='rating3'),
    url(r'^rating4/(?P<pk>[0-9]+)/$', views.rating4, name='rating4'),
    url(r'^rating5/(?P<pk>[0-9]+)/$', views.rating5, name='rating5'),

]
