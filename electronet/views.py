import decimal
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from electronet.models import Product, Company, Delivery, Debt, DeliveryNet
from electronet.serializers import ProductSerializer, CompanySerializer, DeliverySerializer, DebtSerializer, \
    DeliveryNetSerializer
from users.permissions import IsActiveUser
from rest_framework.response import Response
from electronet.constants import TYPE_PLANT
from django_filters.rest_framework import DjangoFilterBackend


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]


class ProductRetriveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]

    def perform_update(self, serializer):
        product = serializer.save()
        if not product.is_active:
            # деактивировать цепочку
            dlv_net = DeliveryNet.objects.filter(product=product.pk)
            for item in dlv_net:
                item.is_active = False
                item.save()
        product.save()


class CompanyListAPIView(generics.ListAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['country', ]


class CompanyCreateAPIView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]


class CompanyRetriveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]

    def perform_update(self, serializer):
        company = serializer.save()
        if not company.is_active:
            # деактивировать цепочку
            if company:
                for item in DeliveryNet.objects.filter(supplier=company.pk):
                    for elm in DeliveryNet.objects.filter(product=item.product.pk):
                        if elm.level >= item.level:
                            elm.is_active = False
                            elm.save()
        company.save()


class DebtViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DebtSerializer
    queryset = Debt.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]

class DeliveryAPIView(generics.ListCreateAPIView):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]

    def post(self, request, *args, **kwargs):
        delivery_net_id = self.request.data.get('delivery_net')
        value = decimal.Decimal(self.request.data.get('value'))
        dlv_net = DeliveryNet.objects.filter(pk=delivery_net_id).first()
        if dlv_net:
            if not dlv_net.is_active:
                return Response({"message": 'Элемент сети деактивирован, поставка невозможна'})
            delivery = Delivery.objects.create(delivery_net=dlv_net, value=value, created_by=request.user)
            delivery.save()
            debt = Debt.objects.filter(company_id=dlv_net.company.pk,
                                       supplier_id=dlv_net.supplier.pk).first()
            if not debt:
                debt = Debt.objects.create(company_id=dlv_net.company.pk,
                                           supplier_id=dlv_net.supplier.pk)
            debt.debt += value
            debt.save()
        else:
            return Response({"message": 'Элемент сети не существует, поставка невозможна'})
        return Response({"message": 'Поставка добавлена'})


class DeliveryNetListAPIView(generics.ListAPIView):
    serializer_class = DeliveryNetSerializer
    queryset = DeliveryNet.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]


class DeliveryNetCreateAPIView(generics.CreateAPIView):
    serializer_class = DeliveryNetSerializer
    queryset = DeliveryNet.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]

    def post(self, request, *args, **kwargs):
        product_id = self.request.data.get('product')
        supplier_id = self.request.data.get('supplier')
        company_id = self.request.data.get('company')
        product = Product.objects.filter(pk=product_id).first()
        supplier = Company.objects.filter(pk=supplier_id).first()
        company = Company.objects.filter(pk=company_id).first()
        if not product or not product.is_active:
            return Response({"message": 'Продукт не существует или деактвирован'})
        if not supplier or not supplier.is_active:
            return Response({"message": 'Поставщик не существует или деактвирован'})
        if not company or not company.is_active or company.type == TYPE_PLANT:
            return Response({"message": 'Получатель не существует или деактвирован'})
        network = DeliveryNet.objects.filter(product=product.pk)
        if network:
            # добавить
            sorted_network = sorted(network, key=lambda x: x.level)
            for item in sorted_network:
                if item.company == company and item.company.is_active:
                    return Response({"message": 'Для этого элемента уже есть поставщик'})
                if item.supplier == supplier and item.company.is_active:
                    return Response({"message": 'Для этого поставщика уже есть покупатель'})
            for item in sorted_network:
                level = item.level + 1
                if item.company == supplier:
                    delivery_net = DeliveryNet.objects.create(supplier=supplier, company=company, product=product,
                                                              is_active=True, level=level)
                    delivery_net.save()
                    return Response({"message": 'Элемент сети поставщика добавлен'})
        else:
            # создать сеть
            level = 1
            if supplier == product.manufacturer:
                delivery_net = DeliveryNet.objects.create(supplier=supplier, company=company, product=product,
                                                          is_active=True, level=level)
                delivery_net.save()
                return Response({"message": 'Элемент сети поставщика добавлен'})
            else:
                return Response({"message": 'продукт не существует или деактвирован'})


class DeliveryNetRetriveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = DeliveryNetSerializer
    queryset = DeliveryNet.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]

    def put(self, request, *args, **kwargs):
        product_id = self.request.data.get('product')
        supplier_id = self.request.data.get('supplier')
        company_id = self.request.data.get('company')
        is_active = self.request.data.get('is_active')
        product = Product.objects.filter(pk=product_id).first()
        supplier = Company.objects.filter(pk=supplier_id).first()
        company = Company.objects.filter(pk=company_id).first()
        deliverynet = DeliveryNet.objects.filter(supplier=supplier, company=company, product=product).first()
        if deliverynet:
            if deliverynet.is_active == is_active:
                return Response({"message": 'Без изменений'})
            else:
                if not is_active:
                    # деактивировать сеть
                    network = DeliveryNet.objects.filter(product=product.pk)
                    if network:
                        sorted_network = sorted(network, key=lambda x: x.level)
                        for item in sorted_network:
                            if item.level > deliverynet.level:
                                item.is_active = False
                                item.save()
                deliverynet.is_active = is_active
                deliverynet.save()
                return Response({"message": 'Элемент успешно изменен'})
        else:
            return Response({"message": 'Элемент сети поставщика не существует'})

    def patch(self, request, *args, **kwargs):
        product_id = self.request.data.get('product')
        supplier_id = self.request.data.get('supplier')
        company_id = self.request.data.get('company')
        is_active = self.request.data.get('is_active')
        product = Product.objects.filter(pk=product_id).first()
        supplier = Company.objects.filter(pk=supplier_id).first()
        company = Company.objects.filter(pk=company_id).first()
        deliverynet = DeliveryNet.objects.filter(supplier=supplier, company=company, product=product).first()
        if deliverynet:
            if deliverynet.is_active == is_active:
                return Response({"message": 'Без изменений'})
            else:
                if not is_active:
                    # деактивировать сеть
                    network = DeliveryNet.objects.filter(product=product.pk)
                    if network:
                        sorted_network = sorted(network, key=lambda x: x.level)
                        for item in sorted_network:
                            if item.level > deliverynet.level:
                                item.is_active = False
                                item.save()
                deliverynet.is_active = is_active
                deliverynet.save()
                return Response({"message": 'Элемент успешно изменен'})
        else:
            return Response({"message": 'Элемент сети поставщика не существует'})
