# Generated by Django 2.2.4 on 2019-10-08 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='currency',
            field=models.CharField(blank=True, choices=[('USD', 'Dolares'), ('VEF', 'Bolivares')], max_length=2, null=True, verbose_name='Unidad de medida'),
        ),
    ]
