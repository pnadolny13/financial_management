try:
    from django.urls import url
except ImportError:
    from django.conf.urls import url

from . import views
from .views import ZeroConfigurationDatatableView

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^zero-configuration/$', ZeroConfigurationDatatableView.as_view(), name='zero-configuration')
]
