# Generated by Django 3.2.4 on 2021-07-26 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20210724_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Общая цена'),
        ),
    ]