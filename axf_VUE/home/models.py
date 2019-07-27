from django.db import models

# Create your models here.

class MainBase(models.Model):

    img = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    trackid = models.IntegerField(default=0)

    class Meta:
        abstract=True

class MainWheel(MainBase):
    class Meta:
        db_table = "axf_wheel"

class MainNav(MainBase):
    class Meta:
        db_table = "axf_nav"

class MainMustBuy(MainBase):
    class Meta:
        db_table = "axf_mustbuy"


class MainShop(MainBase):
    class Meta:
        db_table = "axf_shop"


class MainShow(MainBase):
    """
    axf_mainshow(trackid,name,img,categoryid,brandname,img1,childcid1,productid1,longname1,price1,marketprice1,
    img2,childcid2,productid2,longname2,price2,marketprice2,img3,childcid3,productid3,longname3,price3,marketprice3)
    """
    categoryid = models.IntegerField(default=1)
    brandname = models.CharField(max_length=64)
    img1 = models.CharField(max_length=255)
    childcid1 = models.IntegerField(default=0)
    productid1 = models.IntegerField(default=0)
    longname1 = models.CharField(max_length=128)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=0)
    img2 = models.CharField(max_length=255)
    childcid2 = models.IntegerField(default=1)
    productid2 = models.IntegerField(default=1)
    longname2 = models.CharField(max_length=128)
    price2 = models.FloatField(default=1)
    marketprice2 = models.FloatField(default=0)
    img3 = models.CharField(max_length=255)
    childcid3 = models.IntegerField(default=1)
    productid3 = models.IntegerField(default=1)
    longname3 = models.CharField(max_length=128)
    price3 = models.FloatField(default=1)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = 'axf_mainshow'






