from rest_framework import viewsets, generics
from electronet.models import Product, Company, Deliveries
from electronet.serializers import ProductSerializer, CompanySerializer, DeliveriesSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class DeliveriesViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveriesSerializer
    queryset = Deliveries.objects.all()
