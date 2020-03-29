try:
    from django.urls import url
except ImportError:
    from django.conf.urls import url

from . import views
from .views import SpendingTrackerDatatableView

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^spending_tracker/$', SpendingTrackerDatatableView.as_view(), name='spending_tracker')
]
