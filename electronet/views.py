from rest_framework import viewsets, generics
from electronet.models import Product, Company, Delivery, Debt
from electronet.serializers import ProductSerializer, CompanySerializer, DeliverySerializer, DebtSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


# class DeliveryViewSet(viewsets.ModelViewSet):
class DebtViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DebtSerializer
    queryset = Debt.objects.all()
