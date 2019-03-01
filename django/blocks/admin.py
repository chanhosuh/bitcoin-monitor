from django.contrib import admin

from blocks.models import Block
from transactions.models import Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction


class BlockAdmin(admin.ModelAdmin):
    inlines = [
        TransactionInline,
    ]
    list_display = ('height', 'age', 'confirmations', 'number_of_transactions', 'hash')
    list_display_links = ('height', 'hash')
    search_fields = ('hash', 'height')
    list_per_page = 25


admin.site.register(Block, BlockAdmin)
