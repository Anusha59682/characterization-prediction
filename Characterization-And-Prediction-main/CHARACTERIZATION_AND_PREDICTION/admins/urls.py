from django.conf.urls import url
from admins import views

app_name = 'admins'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^upload/products/$', views.uploadproducts, name='uploadproducts'),
    url(r'^charts/(?P<chart_type>\w+)/$', views.charts, name='charts'),
    url(r'^charts1/(?P<chart_type>\w+)/$', views.charts1, name='charts1'),
    url(r'^charts2/(?P<chart_type>\w+)/$', views.charts2, name='charts2'),
    url(r'^charts3/(?P<chart_type>\w+)/$', views.charts3, name='charts3'),
    url(r'^delete_product/(?P<id>\d+)/$', views.delete_product, name='delete_product'),
    url(r'^logout/$', views.logout, name='logout'),
]