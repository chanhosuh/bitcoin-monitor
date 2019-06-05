from django.contrib import admin

from transactions.models import Transaction, TransactionInput, TransactionOutput


class OutputInline(admin.TabularInline):
    model = TransactionOutput


class InputInline(admin.TabularInline):
    model = TransactionInput


class TransactionAdmin(admin.ModelAdmin):
    inlines = [
        InputInline,
        OutputInline,
    ]


admin.site.register(Transaction, TransactionAdmin)
