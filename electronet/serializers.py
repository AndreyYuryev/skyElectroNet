from rest_framework import serializers
from electronet.models import Company, Product, Deliveries
from electronet.utils import COMPANY_TYPE, TYPE_PLANT, TYPE_RETAIL, TYPE_ENTREPRENEUR


class CompanySerializer(serializers.ModelSerializer):
    is_manufacturer = serializers.SerializerMethodField()

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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class DeliveriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliveries
        fields = "__all__"
        read_only_fields = ['debt', 'level', ]
        # extra_kwargs = {
        #     'debt': {'write_only': True},
        # }
