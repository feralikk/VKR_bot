# Generated by Django 3.0.6 on 2020-05-27 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparser', '0011_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='external_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='Внешний ID пользователя'),
        ),
    ]