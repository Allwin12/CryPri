# Generated by Django 2.2.1 on 2019-05-07 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Additional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_source', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
    ]