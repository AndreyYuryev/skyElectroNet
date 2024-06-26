# Generated by Django 5.0.6 on 2024-05-30 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronet', '0014_alter_deliverynet_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverynet',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='элемент сети активен'),
        ),
        migrations.AlterField(
            model_name='deliverynet',
            name='level',
            field=models.IntegerField(default=0, verbose_name='уровень в иерархии сети'),
        ),
    ]
