# Generated by Django 2.2.4 on 2019-09-11 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raw_materials', '0004_auto_20190911_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawmaterial',
            name='time_to_expire',
            field=models.DurationField(blank=True, null=True, verbose_name='Tiempo aproximado en expirar'),
        ),
    ]
