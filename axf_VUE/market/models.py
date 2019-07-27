from django.db import models

# Create your models here.
class Goods(models.Model):
    """
    axf_goods(productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,marketprice,categoryid,
    childcid,childcidname,dealerid,storenums,productnum) values("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q",
    "","乐吧薯片鲜虾味50.0g",0,0,"50g",2.00,2.500000,103541,103543,"膨化食品","4858",200,4)

    """
    productid = models.IntegerField(default=1)
    productimg = models.CharField(max_length=255)
    productname = models.CharField(max_length=128)
    productlongname = models.CharField(max_length=255)
    isxf = models.BooleanField(default=False)
    pmdesc = models.BooleanField(default=False)
    specifics = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    categoryid = models.IntegerField(default=1)
    childcid = models.IntegerField(default=1)
    childcidname = models.CharField(max_length=128)
    dealerid = models.IntegerField(default=1)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_goods'

class FoodType(models.Model):
    """
    axf_foodtype(typeid,typename,childtypenames,typesort)
    """

    typeid = models.IntegerField(default=1)
    typename = models.CharField(max_length=32)
    childtypenames = models.CharField(max_length=255)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtype'