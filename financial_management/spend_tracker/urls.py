from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views
from .views import TransactionsDatatableView, BudgetDatatableView, DownloadView

urlpatterns = [
    path('', TransactionsDatatableView.as_view(), name='transactions'),
    path('budget/', BudgetDatatableView.as_view(), name='budget'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('download/', DownloadView.as_view(), name='download')
]
