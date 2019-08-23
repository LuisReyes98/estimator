# Generated by Django 2.2.4 on 2019-08-23 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('raw_materials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialSaleRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField(verbose_name='Amount')),
                ('cost_dollar', models.FloatField(verbose_name='Cost in Dollars')),
                ('cost_local', models.FloatField(verbose_name='Cost in the local coin')),
                ('raw_material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sold_ocassions', to='raw_materials.RawMaterial', verbose_name='Raw Material')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('total_cost_dollar', models.FloatField(verbose_name='Total sale cost in Dollars')),
                ('total_cost_local', models.FloatField(verbose_name='Total sale cost in the local coin')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link=True, to='users.Company')),
                ('company_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link=True, to='users.CompanyUser')),
                ('raw_materials', models.ManyToManyField(through='sales.MaterialSaleRelation', to='raw_materials.RawMaterial', verbose_name='Raw Materials')),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.AddField(
            model_name='materialsalerelation',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold_materials', to='sales.Sale', verbose_name='Sale'),
        ),
    ]
