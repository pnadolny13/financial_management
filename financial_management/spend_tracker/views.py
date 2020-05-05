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
from .models import Budget, BudgetRule, Transaction, TransactionCategory


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


class MonthBudgetStatus(LoginRequiredMixin, TemplateView):
    template_name = 'month_budget_status.html'


class MonthBudgetChart(LoginRequiredMixin, View):

    def get(self, request):
        labels = []
        data = []
        budget_data = []
        today = datetime.date.today()
        _, num_days = calendar.monthrange(today.year, today.month)
        start_date = datetime.date(today.year, today.month, 1)
        end_date = datetime.date(today.year, today.month, num_days)
        # Sum of spent by category lookup
        spent_per_category = Transaction.objects.values('transaction_category').annotate(total_spent=Sum('amount')).filter(transaction_at__range=(start_date, end_date))
        spent_lookup = {}
        for spent in spent_per_category:
            spent_lookup[spent.get('transaction_category')] = spent.get('total_spent')
        # Budget amount by category lookup
        budget_lookup = {}
        bud = Budget.objects.values('id').filter(user_id=request.user)
        if bud:
            bud_id = bud[0]['id']
            category_budget_rules = BudgetRule.objects.values('transaction_category', 'max_spend_rule').filter(budget_id=bud_id)
            for rule in category_budget_rules:
                budget_lookup[rule.get('transaction_category')] = rule.get('max_spend_rule')
        # Add spent and budget by category to data
        categories = TransactionCategory.objects.values('name', 'id')
        for category in categories:
            labels.append(category['name'])
            data.append(spent_lookup.get(category['id']))
            budget_data.append(budget_lookup.get(category['id']))
        return JsonResponse(data={
            'labels': labels,
            'spent_data': data,
            'budget_data': budget_data
        })
