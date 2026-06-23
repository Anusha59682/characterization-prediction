from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from CHARACTERIZING_AND_PREDICTING import settings
from user import views as user_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admins/', include('admins.urls', namespace='admins')),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^$', user_views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)