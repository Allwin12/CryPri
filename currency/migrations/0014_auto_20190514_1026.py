# Generated by Django 2.2.1 on 2019-05-14 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0013_maintable_coinid'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintable',
            name='onehourchange',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='maintable',
            name='sevendaychange',
            field=models.FloatField(null=True),
        ),
    ]
