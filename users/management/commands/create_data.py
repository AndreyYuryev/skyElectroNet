from django.core.management import BaseCommand
from electronet.models import Product, Company, DeliveryNet


class Command(BaseCommand):
    def handle(self, *args, **options):
        plant = Company.objects.create(
        name = 'Plant_a',
        email = 'plant_a@sky.pro',
        country = 'Россия',
        type = 'P')
        plant.save()
        retail1 = Company.objects.create(
            name='Retail_a',
            email='Retail_a@sky.pro',
            country='Россия',
            type='R')
        retail1.save()
        retail2 = Company.objects.create(
            name='Retail_b',
            email='Retail_b@sky.pro',
            country='Казахстан',
            type='R')
        retail2.save()
        ent1 = Company.objects.create(
            name='ИП Сидоров',
            email='sidorov@sky.pro',
            country='Казахстан',
            type='E')
        ent1.save()
        ent2= Company.objects.create(
            name='ИП Кузнецов',
            email='smith@sky.pro',
            country='Россия',
            type='E')
        ent2.save()
        product1 = Product.objects.create(
            model ='M001',
        name = 'Продукт 1',
        description = 'Электронный продукт 1',
        manufacturer = plant)
        product1.save()
        product2 = Product.objects.create(
            model ='M002',
        name = 'Продукт 2',
        description = 'Электронный продукт 2',
        manufacturer = plant)
        product2.save()
        dlv_el1 = DeliveryNet.objects.create(supplier=plant, company=retail1, product=product1, level=1)
        dlv_el1.save()
        dlv_el2 = DeliveryNet.objects.create(supplier=retail1, company=retail2, product=product1, level=2)
        dlv_el2.save()
        dlv_el3 = DeliveryNet.objects.create(supplier=retail2, company=ent1, product=product1, level=3)
        dlv_el3.save()
        dlv_el4 = DeliveryNet.objects.create(supplier=plant, company=retail2, product=product2, level=1)
        dlv_el4.save()
        dlv_el5 = DeliveryNet.objects.create(supplier=retail2, company=ent1, product=product2, level=2)
        dlv_el5.save()

