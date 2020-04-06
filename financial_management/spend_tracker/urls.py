from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views
from .views import TransactionsDatatableView

urlpatterns = [
    path('', TransactionsDatatableView.as_view(), name='transactions'),
    path('accounts/', include('django.contrib.auth.urls')),
]
