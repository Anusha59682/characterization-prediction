from django.conf.urls import url
from vendor import views

app_name = 'vendor'

urlpatterns = [
    url(r'^$', views.home, name='home'),
]