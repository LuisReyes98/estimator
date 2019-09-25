# Generated by Django 2.2.4 on 2019-09-25 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_auto_20190924_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='dollar_price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.DolarPrice', verbose_name='Precio del dolar'),
        ),
    ]