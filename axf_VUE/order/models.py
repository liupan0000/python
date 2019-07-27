import datetime

from django.db import models

# Create your models here.
from users.models import userModel

ORDERED_NOT_PAY = 0
ORDERED_PAYED = 1
class OrderModel(models.Model):
    o_user = models.ForeignKey(userModel)
    o_status = models.IntegerField(default=ORDERED_NOT_PAY)
    o_price = models.FloatField(default=0)
    o_ordered_time = models.DateTimeField(auto_created=True,default=datetime.datetime.now())

class OrderGoodsInfo(models.Model):
    productid = models.IntegerField(default=0)
    productimg = models.CharField(max_length=256)
    productname = models.CharField(max_length=128)
    productlongname = models.CharField(max_length=256)
    isxf = models.BooleanField(default=0)
    pmdesc = models.BooleanField(default=0)

    specifics = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    categoryid = models.IntegerField(default=0)
    childcid = models.IntegerField(default=0)
    childcidname = models.CharField(max_length=256)
    dealerid = models.IntegerField(default=0)
    storenums = models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)
    o_goods = models.OneToOneField('OrderGoods')

class OrderGoods(models.Model):
    o_order = models.ForeignKey(OrderModel)
    o_goods_num = models.IntegerField(default=1)
