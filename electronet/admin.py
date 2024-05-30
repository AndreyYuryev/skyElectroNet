from django.contrib import admin
from electronet.models import Product, Company, DeliveryNet, Debt, Delivery, Payment
from electronet.utils import create_hierarchy
from electronet.constants import TYPE_PLANT, TYPE_RETAIL, TYPE_ENTREPRENEUR
from django.contrib import messages


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country', 'city', 'street', 'house', 'type', 'is_active',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["type", ]
        else:
            return []

    def has_delete_permission(self, request, obj=None):
        return False


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

    def save_model(self, request, obj, form, change):
        """ Дективировать цепочку поставки с завода для продукта"""
        if not obj.is_active:
            product = Product.objects.filter(pk=obj.pk).first()
            if product:
                dlv_net = DeliveryNet.objects.filter(product=obj.pk, level=1)
                for item in dlv_net:
                    item.is_active = False
                    item.save()
        super().save_model(request, obj, form, change)


@admin.register(DeliveryNet)
class DeliveryNetAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'company', 'product', 'level', 'is_active',)
    fields = ('supplier', 'company', 'product', 'level', 'is_active',)
    ordering = ['product', 'level', ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['company', 'supplier', 'product', 'level']
        else:
            return ['level', ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company":
            kwargs["queryset"] = Company.objects.filter(type__in=[TYPE_RETAIL, TYPE_ENTREPRENEUR], is_active=True)
            # print(kwargs)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'supplier':
            kwargs["queryset"] = Company.objects.filter(is_active=True)
            # print(kwargs)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'product':
            kwargs["queryset"] = Product.objects.filter(is_active=True)
            #     print(kwargs)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """ Обработать создание/изменение элемента сети """
        success = False
        msg = ''
        level = 0
        company_from_pk = obj.supplier.pk
        company_to_pk = obj.company.pk
        product_pk = obj.product.pk
        obj_is_active = obj.is_active
        success, msg, level = create_hierarchy(company_from_pk, company_to_pk, product_pk, obj_is_active)
        if not success:
            messages.set_level(request, messages.ERROR)
            messages.add_message(request, messages.ERROR, msg)
            return False
        else:
            obj.level = level
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_net', 'value', 'created_at', 'created_by',)
    readonly_fields = ('created_by',)

    def get_fields(self, request, obj=None):
        if obj:
            return ['delivery_net', 'value', 'created_at', 'created_by', ]
        else:
            return ['delivery_net', 'value', ]

    def save_model(self, request, obj, form, change):
        debt = Debt.objects.filter(company_id=obj.delivery_net.company_id,
                                   supplier_id=obj.delivery_net.supplier_id).first()
        if not debt:
            debt = Debt.objects.create(company_id=obj.delivery_net.company_id, supplier_id=obj.delivery_net.supplier_id)
        debt.debt += obj.value
        debt.save()
        obj.created_by = request.user
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

    @admin.action(description="Списать задолженность перед поставщиком/Оплатить")
    def clear_debt(self, request, queryset):
        for debt in queryset:
            payment = Payment.objects.create(company=debt.company, supplier=debt.supplier, payment=debt.debt,
                                             created_by=request.user)
            if payment:
                payment.save()
                queryset.update(debt=0)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'company', 'payment', 'created_at', 'created_by',)
    readonly_fields = ('supplier', 'company', 'payment', 'created_at', 'created_by',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
