# -*- encoding: utf-8 -*-

from os import sep
import os.path
import re
import django
from django.urls import reverse
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect

import datatableview
from datatableview import Datatable
from datatableview.views import DatatableView

from .models import Transaction
from .forms import TransactionForm


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        # Try to determine if the user jumped the gun on testing things out
        db_works = True
        try:
            list(Entry.objects.all()[:1])
        except:
            db_works = False
        context['db_works'] = db_works

        path, working_directory = os.path.split(os.path.abspath('.'))
        context['working_directory'] = working_directory
        context['os_sep'] = sep

        # Versions
        context.update({
            'datatableview_version': '.'.join(map(str, datatableview.__version_info__)),
            'django_version': django.get_version(),
            'datatables_version': '1.10.9',
        })

        return context


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
class TransactionsDatatableView(PermissionRequiredMixin, BasicMixin, DatatableView):
    """
    If no columns are specified by the view's ``Datatable`` configuration object (or no
    ``datatable_class`` is given at all), ``DatatableView`` will use all of the model's local
    fields.  Note that this does not include reverse relationships, many-to-many fields (even if the
    ``ManyToManyField`` is defined on the model directly), nor the special ``pk`` field, but DOES
    include ``ForeignKey`` fields defined directly on the model.

    Note that fields will automatically use their ``verbose_name`` for the frontend table headers.

    WARNING:
    When no columns list is explicitly given, the table will end up trying to show foreign keys as
    columns, generating at least one extra query per displayed row.  Implement a ``get_queryset()``
    method on your view that returns a queryset with the appropriate call to ``select_related()``.
    """
    permission_required = ''
    # redirect_field_name = 'transactions'
    model = Transaction
    datatable_class = TransactionDatatable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TransactionForm()
        context['form'] = form
        return context

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            Transaction.objects.create(
                user_id=form.cleaned_data['user'],
                transaction_type=form.cleaned_data['type'],
                transaction_category=form.cleaned_data['category'],
                amount=form.cleaned_data['amount'],
                description=form.cleaned_data['description'],
                forecast_transaction_flag=False
            )
        return HttpResponseRedirect('/')
