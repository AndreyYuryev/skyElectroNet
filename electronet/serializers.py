from rest_framework import serializers
from electronet.models import Company, Product, Delivery, Debt, DeliveryNet
from electronet.constants import COMPANY_TYPE, TYPE_PLANT, TYPE_RETAIL, TYPE_ENTREPRENEUR


class CompanySerializer(serializers.ModelSerializer):
    is_manufacturer = serializers.SerializerMethodField()
    type_company = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = [
            'type', 'created_at',
        ]

    def get_is_manufacturer(self, instance):
        if instance.type == TYPE_PLANT:
            return True

    def get_type_company(self, instance):
        for item in COMPANY_TYPE:
            if item[0] == instance.type:
                return item[1]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = [
            'model', 'manufaturef', 'launch_date',
        ]


class DeliverySerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Delivery
        fields = "__all__"


class DebtSerializer(serializers.ModelSerializer):
    company_from = serializers.SerializerMethodField()
    company_to = serializers.SerializerMethodField()

    class Meta:
        model = Debt
        fields = ['supplier', 'company_from', 'company', 'company_to', 'debt', ]

    def get_company_from(self, instance):
        return Company.objects.filter(pk=instance.supplier.pk).first().name

    def get_company_to(self, instance):
        return Company.objects.filter(pk=instance.company.pk).first().name


class DeliveryNetSerializer(serializers.ModelSerializer):
    company_from = serializers.SerializerMethodField()
    company_to = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = DeliveryNet
        fields = ['id', 'supplier', 'company_from', 'company', 'company_to', 'product', 'product_name', 'level',
                  'is_active']
        read_only_fields = [
            'id', 'supplier', 'company_from', 'company', 'company_to', 'product', 'product_name', 'level',
        ]

    def get_company_from(self, instance):
        return Company.objects.filter(pk=instance.supplier.pk).first().name

    def get_company_to(self, instance):
        return Company.objects.filter(pk=instance.company.pk).first().name

    def get_product_name(self, instance):
        return Product.objects.filter(pk=instance.product.pk).first().name
