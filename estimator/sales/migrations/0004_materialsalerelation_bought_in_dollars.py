# Generated by Django 2.2.4 on 2019-09-25 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_sale_dollar_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialsalerelation',
            name='bought_in_dollars',
            field=models.BooleanField(default=False, verbose_name='Comprado en dolares'),
        ),
    ]