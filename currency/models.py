from django.db import models

class crontab(models.Model):
    name = models.CharField(max_length=20)


class converter(models.Model):
    name = models.CharField(max_length=20)

class MainTable(models.Model):
    rank = models.IntegerField(null=True)
    coinid = models.CharField(max_length=30,null=True)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    thumbimg = models.CharField(max_length=30)
    marketcap = models.FloatField(null=True)
    totalvolume = models.FloatField(null=True)
    price_change = models.FloatField(null=True)
    pricechangepercentage = models.FloatField(null=True)
    onehourchange = models.FloatField(null=True)
    sevendaychange = models.FloatField(null=True)
    circulating_supply = models.FloatField(null=True)

class Table(models.Model):
    name = models.CharField(max_length=30)
    coinid = models.CharField(max_length=30)
    symbol = models.CharField(max_length=20)
    img = models.CharField(max_length=50)
    image = models.CharField(max_length=50)

class Price(models.Model):
    price = models.FloatField(null=True)

class Marketdata(models.Model):
    price_change_24h = models.FloatField(null=True)
    price_change_percentage_24h = models.FloatField(null=True)