# Generated by Django 4.1.2 on 2022-11-24 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='numero',
            field=models.IntegerField(default=0, null=True),
        ),
    ]