from django.contrib import admin

from transactions.models import CoinbaseTransaction, Transaction, TransactionInput, TransactionOutput


class OutputInline(admin.TabularInline):
    model = TransactionOutput


class InputInline(admin.TabularInline):
    model = TransactionInput


class CoinbaseInline(admin.TabularInline):
    model = CoinbaseTransaction


class TransactionAdmin(admin.ModelAdmin):
    inlines = [
        CoinbaseInline,
        InputInline,
        OutputInline,
    ]


admin.site.register(Transaction, TransactionAdmin)
