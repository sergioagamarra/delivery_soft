# Generated by Django 4.1.2 on 2022-11-24 21:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]