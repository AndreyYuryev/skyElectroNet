# Generated by Django 5.0.6 on 2024-05-30 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronet', '0013_alter_delivery_created_at_alter_delivery_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverynet',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='элемент сети поставки активен'),
        ),
    ]