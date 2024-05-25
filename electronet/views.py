from rest_framework import viewsets, generics
from electronet.models import Product, Company
from electronet.serializers import ProductSerializer, CompanySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


# class DeliveriesViewSet(viewsets.ModelViewSet):
#     serializer_class = DeliveriesSerializer
#     queryset = Deliveries.objects.all()
