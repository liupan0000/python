from django.db import models

# Create your models here.
from market.models import Goods
from users.models import userModel


class CartModel(models.Model):

    c_user = models.ForeignKey(userModel)
    c_goods = models.ForeignKey(Goods)
    c_goods_num = models.IntegerField(default=1)
    c_is_select =models.BooleanField(default=True)
