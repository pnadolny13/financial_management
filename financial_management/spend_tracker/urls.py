try:
    from django.urls import url
except ImportError:
    from django.conf.urls import url

from . import views
from .views import TransactionsDatatableView

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^transactions/$', TransactionsDatatableView.as_view(), name='spending_tracker')
]
