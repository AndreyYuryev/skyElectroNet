from rest_framework import serializers
from electronet.models import Company, Product, Delivery, Debt
from electronet.constants import COMPANY_TYPE, TYPE_PLANT, TYPE_RETAIL, TYPE_ENTREPRENEUR


class CompanySerializer(serializers.ModelSerializer):
    is_manufacturer = serializers.SerializerMethodField()
    type_company = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }
        # read_only_fields = [
        #     'is_staff', 'is_superuser', 'is_active',
        #     # 'date_joined', 'last_login', 'groups', 'user_permissions',
        # ]

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


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class DebtSerializer(serializers.ModelSerializer):
    company_from = serializers.SerializerMethodField()
    company_to = serializers.SerializerMethodField()

    class Meta:
        model = Debt
        fields = ['supplier', 'company_from', 'company',  'company_to', 'debt', ]

    def get_company_from(self, instance):
        return Company.objects.filter(pk=instance.supplier.pk).first().name

    def get_company_to(self, instance):
        return Company.objects.filter(pk=instance.company.pk).first().name
# class DeliveriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Deliveries
#         fields = "__all__"
#         read_only_fields = ['debt', 'level', ]
#         # extra_kwargs = {
#         #     'debt': {'write_only': True},
#         # }
