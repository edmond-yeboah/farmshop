# Generated by Django 4.0.1 on 2022-05-24 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_product_added_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='score',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]