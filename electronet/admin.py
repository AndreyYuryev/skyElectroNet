from django.contrib import admin
from electronet.models import Product, Company, DeliveryNet, Debt, Delivery, Payment
from electronet.utils import TYPE_PLANT, TYPE_RETAIL, TYPE_ENTREPRENEUR
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


@admin.register(DeliveryNet)
class DeliveryNetAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'company', 'product', 'level', 'is_active',)
    fields = ('supplier', 'company', 'product', 'level', 'is_active',)

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
        company_from = obj.supplier.pk
        company_to = obj.company.pk
        product = obj.product.pk
        dlv = DeliveryNet.objects.filter(company=company_to, supplier=company_from, product=product).first()
        if dlv:
            if not obj.is_active:
                print('Деактивировать цепочку')
            elif dlv.is_active != obj.is_active:
                print('Активировать элемент')
            else:
                messages.set_level(request, messages.ERROR)
                messages.add_message(request, messages.ERROR, 'Элемент сети существует')
                return False
        # net = DeliveryNet.objects.filter(product=obj.product.pk)
        # for item in net:
        #     if item.supplier.pk == company_from:
        #         messages.add_message(request, messages.ERROR, 'Для компании уже есть поставщик')
        #         return False
        # print('!o', obj, '!f', form, '!c', change)
        # if obj.company.type != TYPE_PLANT:
        #     super().save_model(request, obj, form, change)
        # else:
        #     messages.add_message(request, messages.ERROR, 'Завод не может выступать в роли получателя')
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
    list_display = ('supplier', 'company', 'payment', 'created_at', 'created_by',)
    readonly_fields = ('supplier', 'company', 'payment', 'created_at', 'created_by',)

    # actions = ['clear_debt', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
