# Generated by Django 2.2.4 on 2019-10-01 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_salefile'),
    ]

    operations = [
        migrations.AddField(
            model_name='dolarprice',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
