# Generated by Django 3.2.9 on 2022-01-17 00:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_alter_shopuser_activation_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 19, 0, 36, 11, 4902)),
        ),
        migrations.DeleteModel(
            name='ShopUserProfile',
        ),
    ]
