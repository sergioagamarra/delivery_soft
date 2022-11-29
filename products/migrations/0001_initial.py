# Generated by Django 4.1.3 on 2022-11-23 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('image', models.CharField(max_length=200)),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='products.category')),
            ],
        ),
    ]