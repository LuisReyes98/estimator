# Generated by Django 2.2.4 on 2019-09-18 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('raw_materials', '0005_auto_20190911_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Company', verbose_name='Compañía'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='rawmaterial',
            name='providers',
            field=models.ManyToManyField(through='raw_materials.MaterialProvider', to='raw_materials.Provider', verbose_name='Proveedores'),
        ),
    ]
