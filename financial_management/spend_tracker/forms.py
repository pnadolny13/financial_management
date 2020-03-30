from django import forms
from .models import TransactionType, TransactionCategory
from django.contrib.auth import get_user_model


class TransactionForm(forms.Form):
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    type = forms.ModelChoiceField(queryset=TransactionType.objects.all())
    category = forms.ModelChoiceField(queryset=TransactionCategory.objects.all())
    amount = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
