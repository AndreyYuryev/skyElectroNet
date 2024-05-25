from django.contrib import admin
from electronet.models import Product, Company, DeliveryNet, Debt, Delivery, Payment
from electronet.utils import TYPE_PLANT
from django.contrib import messages


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country', 'city', 'street', 'house', 'type',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["type", ]
        else:
            return []


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'description', 'launch_date', 'manufacturer', 'is_active',)

    # readonly_fields = ['manufacturer', 'launch_date', ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['model', 'manufacturer', 'launch_date']
        else:
            return []

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DeliveryNet)
class DeliveryNetAdmin(admin.ModelAdmin):
    list_display = ('company', 'supplier', 'product', 'level',)
    readonly_fields = ('level',)

    def save_model(self, request, obj, form, change):
        if obj.company.type != TYPE_PLANT:
            super().save_model(request, obj, form, change)
            # else:
            messages.add_message(request, messages.ERROR, 'Завод не может выступать в роли получателя')


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_net', 'value', 'created_at', 'created_by',)
    readonly_fields = ('created_by',)

    # fields = ('delivery_net', 'value', 'created_at', )

    def get_fields(self, request, obj=None):
        if obj:
            return ['delivery_net', 'value', 'created_at', 'created_by', ]
        else:
            return ['delivery_net', 'value', ]

    def save_model(self, request, obj, form, change):
        debt = Debt.objects.filter(company_id=obj.delivery_net.company_id,
                                   supplier_id=obj.delivery_net.supplier_id).first()
        obj.created_by = request.user
        if debt:
            debt.debt += obj.value
            debt.save()
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('company', 'supplier', 'debt',)
    readonly_fields = ('company', 'supplier', 'debt',)
    actions = ['clear_debt', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return ['company', 'supplier', 'debt']
    #     else:
    #         return []

    @admin.action(description="Очистить задолженность перед поставщиком/Оплатить")
    def clear_debt(self, request, queryset):
        for debt in queryset:
            payment = Payment.objects.create(company=debt.company, supplier=debt.supplier, payment=debt.debt,
                                             created_by=request.user)
            if payment:
                payment.save()
                queryset.update(debt=0)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('company', 'supplier', 'payment', 'created_at', 'created_by',)
    readonly_fields = ('company', 'supplier', 'payment', 'created_at', 'created_by',)

    # actions = ['clear_debt', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
