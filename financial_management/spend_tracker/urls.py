from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views
from .views import IndexView, TransactionsDatatableView

urlpatterns = [
    path('', TransactionsDatatableView.as_view(), name="index"),
    path('transactions/', TransactionsDatatableView.as_view(), name='transactions'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
