# -*- encoding: utf-8 -*-

import os.path
import re
from os import sep

import datatableview
import django
from braces.views import LoginRequiredMixin
from datatableview import Datatable
from datatableview.views import DatatableView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, View

from .forms import TransactionForm
from .models import Transaction


class BasicMixin:

    def get_template_names(self):
        """ Try the view's snake_case name, or else use default simple template. """
        name = self.__class__.__name__.replace("DatatableView", "")
        name = re.sub(r'([a-z]|[A-Z]+)(?=[A-Z])', r'\1_', name)
        return [f"{name}.html"]

    def get_context_data(self, **kwargs):
        context = super(BasicMixin, self).get_context_data(**kwargs)
        return context


class TransactionDatatable(Datatable):
    class Meta:
        model = Transaction
        columns = ['transaction_type', 'amount', 'transaction_category', 'description', 'forecast_transaction_flag', 'transaction_at']
        ordering = ['-id']
        # page_length = 5
        # search_fields = ['blog__name']
        # unsortable_columns = ['n_comments']
        # hidden_columns = ['n_pingbacks']
        structure_template = 'datatableview/default_structure.html'


# Column configurations
class TransactionsDatatableView(LoginRequiredMixin, BasicMixin, DatatableView):
    # permissions
    login_url = "/accounts/login"

    model = Transaction
    datatable_class = TransactionDatatable

    def get_queryset(self):
        queryset = super(TransactionsDatatableView, self).get_queryset()
        return queryset.filter(user_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TransactionForm()
        context['form'] = form
        return context

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            Transaction.objects.create(
                user_id=request.user,
                transaction_type=form.cleaned_data['type'],
                transaction_category=form.cleaned_data['category'],
                amount=form.cleaned_data['amount'],
                description=form.cleaned_data['description'],
                forecast_transaction_flag=False
            )
        return HttpResponseRedirect('/')


class BudgetDatatableView(LoginRequiredMixin, BasicMixin, DatatableView):
    # permissions
    login_url = "/accounts/login"

    model = Transaction
    datatable_class = TransactionDatatable

    def get_queryset(self):
        queryset = super(BudgetDatatableView, self).get_queryset()
        return queryset.filter(user_id=self.request.user)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     form = TransactionForm()
    #     context['form'] = form
    #     return context
