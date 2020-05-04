# -*- encoding: utf-8 -*-

import calendar
import datetime
import os.path
import re
from os import sep

import datatableview
import django
from braces.views import LoginRequiredMixin
from datatableview import Datatable, helpers
from datatableview.views import DatatableView, XEditableDatatableView
from django.db.models import Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, View

from .forms import TransactionForm
from .models import Transaction, TransactionCategory


class BasicMixin:

    def get_template_names(self):
        """ Try the view's snake_case name, or else use default simple template. """
        name = self.__class__.__name__.replace("DatatableView", "")
        name = re.sub(r'([a-z]|[A-Z]+)(?=[A-Z])', r'\1_', name)
        name = name.lower()
        return [f"{name}.html"]

    def get_context_data(self, **kwargs):
        context = super(BasicMixin, self).get_context_data(**kwargs)
        return context


class TransactionDatatable(Datatable):
    class Meta:
        columns = [
            'transaction_type', 'amount', 'transaction_category', 'description',
            'forecast_transaction_flag', 'transaction_at']
        ordering = ['-id']
        structure_template = 'datatableview/default_structure.html'
        processors = {
            'amount': helpers.make_xeditable,
            'description': helpers.make_xeditable,
            'forecast_transaction_flag': helpers.make_xeditable,
        }


# Column configurations
class TransactionsDatatableView(LoginRequiredMixin, BasicMixin, XEditableDatatableView):
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
                forecast_transaction_flag=False,
                transaction_at=form.cleaned_data['transaction_at'],
            )
        else:
            super().post(request)
        return HttpResponseRedirect('/')


class BudgetDatatableView(LoginRequiredMixin, BasicMixin, XEditableDatatableView):
    # permissions
    login_url = "/accounts/login"

    model = Transaction
    datatable_class = TransactionDatatable

    def get_queryset(self):
        queryset = super(BudgetDatatableView, self).get_queryset()
        return queryset.filter(user_id=self.request.user)


def spent_per_cat(request):
    return render(request, 'spent_per_cat.html')


def spent_per_cat_calc(request):
    labels = []
    data = []
    today = datetime.date.today()
    _, num_days = calendar.monthrange(today.year, today.month)
    start_date = datetime.date(today.year, today.month, 1)
    end_date = datetime.date(today.year, today.month, num_days)
    queryset = Transaction.objects.values('transaction_category').annotate(toal_spent=Sum('amount')).filter(transaction_at__range=(start_date, end_date))
    for entry in queryset:
        cat_name = TransactionCategory.objects.values('name').get(id=entry['transaction_category'])
        labels.append(cat_name['name'])
        data.append(entry['toal_spent'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
