from django.db import models
from electronet.utils import NULLABLE, COMPANY_TYPE


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    email = models.EmailField(unique=True, verbose_name='почта')
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    street = models.CharField(max_length=255, verbose_name='улица', **NULLABLE)
    house = models.CharField(max_length=32, verbose_name='номер дома', **NULLABLE)
    type = models.CharField(max_length=1, choices=COMPANY_TYPE, verbose_name='тип компании')

    # is_manufacturer = models.BooleanField(default=False, verbose_name='компания-производитель')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='продукт')
    model = models.CharField(max_length=100, verbose_name='модель')
    description = models.CharField(max_length=255, verbose_name='описание продукта', **NULLABLE)
    launch_date = models.DateField(verbose_name='дата выхода на рынок', **NULLABLE)
    manufacturer = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='производитель')

    def __str__(self):
        return f'{self.name} - {self.description}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Deliveries(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='supplier',
                                 verbose_name='поставщик')
    # supplier = models.ManyToManyField(Company, verbose_name='поставщик')
    recipient = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='recipient',
                                  verbose_name='получатель')
    # recipient = models.OneToOneField(Company, on_delete=models.CASCADE, verbose_name='получатель')
    debt = models.DecimalField(decimal_places=2, max_digits=16, verbose_name='задолженность', default=0)
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    level = models.IntegerField(default=1, verbose_name='уровень в иерархии')

    def __str__(self):
        return f'{self.product} supplied from {self.supplier} to {self.recipient}'

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'
