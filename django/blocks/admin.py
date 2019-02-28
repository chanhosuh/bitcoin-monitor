from django.contrib import admin

from blocks.models import Block
from transactions.models import Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction


class BlockAdmin(admin.ModelAdmin):
    inlines = [
        TransactionInline,
    ]


admin.site.register(Block, BlockAdmin)
