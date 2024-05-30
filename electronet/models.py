from django.db import models
from electronet.constants import NULLABLE, COMPANY_TYPE
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    email = models.EmailField(unique=True, verbose_name='почта')
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    street = models.CharField(max_length=255, verbose_name='улица', **NULLABLE)
    house = models.CharField(max_length=32, verbose_name='номер дома', **NULLABLE)
    type = models.CharField(max_length=1, choices=COMPANY_TYPE, verbose_name='тип компании')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    is_active = models.BooleanField(default=True, verbose_name='компания активна')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Product(models.Model):
    model = models.CharField(unique=True, max_length=100, verbose_name='модель')
    name = models.CharField(max_length=100, verbose_name='продукт')
    description = models.CharField(max_length=255, verbose_name='описание продукта', **NULLABLE)
    launch_date = models.DateField(verbose_name='дата выхода на рынок', **NULLABLE)
    manufacturer = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='производитель')
    is_active = models.BooleanField(default=True, verbose_name='продукт производится')


    def __str__(self):
        return f'{self.name} - {self.model}: {self.description}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Debt(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='debt_company', verbose_name='компания')
    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='debt_supplier',
                                 verbose_name='поставщик')
    debt = models.DecimalField(decimal_places=2, max_digits=16, verbose_name='задолженность', default=0)

    def __str__(self):
        return f'Задолженность {self.company} поставщику {self.supplier}'

    class Meta:
        verbose_name = 'Задолженность'
        verbose_name_plural = 'Задолженности'


class Payment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payment_company',
                                verbose_name='компания')
    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payment_supplier',
                                 verbose_name='поставщик')
    payment = models.DecimalField(decimal_places=2, max_digits=16, verbose_name='списание задолженности', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время списания')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Автор',
                                   **NULLABLE)

    def __str__(self):
        return f'Списание задолженности компании {self.company} поставщику {self.supplier}'

    class Meta:
        verbose_name = 'Списание задолженности'
        verbose_name_plural = 'Списание задолженностей'


class DeliveryNet(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='delivery_company',
                                verbose_name='компания')
    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='delivery_supplier',
                                 verbose_name='поставщик')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    level = models.IntegerField(default=0, verbose_name='уровень в иерархии сети')
    is_active = models.BooleanField(default=True, verbose_name='элемент сети активен')

    def __str__(self):
        return f'Поставщик {self.supplier} > получатель {self.company} /{self.product}/ Уровень {self.level}'

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Delivery(models.Model):
    delivery_net = models.ForeignKey(DeliveryNet, on_delete=models.CASCADE, verbose_name='сеть поставщика')
    value = models.DecimalField(decimal_places=2, max_digits=16, verbose_name='сумма поставки', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='автор',
                                   **NULLABLE)

    def __str__(self):
        return f'Поставка на сумму {self.value} {self.delivery_net} '

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'
