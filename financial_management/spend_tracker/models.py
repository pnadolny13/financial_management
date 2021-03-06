# -*- encoding: utf-8 -*-

from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model


class TransactionType(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TransactionCategory(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Transaction categories"


class Transaction(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE, null=False)
    transaction_category = models.ForeignKey('TransactionCategory', on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    description = models.CharField(max_length=1000)
    forecast_transaction_flag = models.BooleanField()
    transaction_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description + ': ' + datetime.strftime(self.created_at, '%Y-%m-%d')


class BudgetRule(models.Model):
    budget_id = models.ForeignKey('Budget', on_delete=models.CASCADE, null=False)
    transaction_category = models.ForeignKey('TransactionCategory', on_delete=models.CASCADE, null=False)
    max_spend_rule = models.DecimalField(decimal_places=2, max_digits=7)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class Budget(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
