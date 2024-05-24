from django.contrib import admin
from electronet.models import Product, Company, Deliveries


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country', 'city', 'street', 'house', 'type', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'description', 'launch_date', 'manufacturer',)


@admin.register(Deliveries)
class DeliveriesAdmin(admin.ModelAdmin):
    list_display = ('product', 'supplier', 'recipient', 'debt', 'level', 'created_at',)
    # list_filter = ('email',)
    # search_fields = ('email', 'first_name', 'last_name',)
    readonly_fields = ['debt', 'level', 'created_at', ]

# actions = ["clear_debt", ]
#
#
# @admin.action(description="Очистить задолженность перед поставщиком")
# def clear_debt(self, request, queryset):
#     # queryset.update(status='published')
#     pass
