# Generated by Django 2.2.1 on 2019-05-08 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0006_delete_additional'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
            ],
        ),
    ]
