from django.contrib import admin

from .models import (Budget, BudgetRule, TransactionCategory, Transaction,
                     TransactionType, User)

admin.site.register(User)
admin.site.register(Budget)
admin.site.register(BudgetRule)
admin.site.register(Transaction)
admin.site.register(TransactionCategory)
admin.site.register(TransactionType)
