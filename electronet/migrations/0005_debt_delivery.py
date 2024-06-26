# Generated by Django 5.0.6 on 2024-05-25 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronet', '0004_alter_product_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debt', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='задолженность')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debt_company', to='electronet.company', verbose_name='компания')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debt_supplier', to='electronet.company', verbose_name='поставщик')),
            ],
            options={
                'verbose_name': 'Задолженность',
                'verbose_name_plural': 'Задолженности',
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_company', to='electronet.company', verbose_name='компания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='electronet.product', verbose_name='продукт')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_supplier', to='electronet.company', verbose_name='поставщик')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
    ]
