# Generated by Django 3.1.4 on 2020-12-20 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laundry', '0006_auto_20201220_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]