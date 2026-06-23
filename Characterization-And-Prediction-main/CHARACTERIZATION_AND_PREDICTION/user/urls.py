from django.conf.urls import url
from user import views

app_name = 'user'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^index/$', views.index, name='index'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^order/(?P<pk>\d+)/$', views.order_detail, name='order_detail'),
    url(r'^ratings/(?P<pk>\d+)/$', views.viewratings, name='ratings'),
    url(r'^addratings/(?P<pk>\d+)/$', views.addratings, name='addratings'),
    url(r'^viewproduct/(?P<pk>\d+)/$', views.viewproduct, name='viewproduct'),
    url(r'^logout/$', views.logout, name='logout'),
]