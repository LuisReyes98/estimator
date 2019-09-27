# Generated by Django 2.2.4 on 2019-09-27 05:55

from django.db import migrations, models
import django.db.models.deletion
import sales.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('sales', '0004_materialsalerelation_bought_in_dollars'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('sale_upload', models.FileField(upload_to=sales.models.get_company_directory_path, verbose_name='Archivo de Registro de Compras')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Company')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]