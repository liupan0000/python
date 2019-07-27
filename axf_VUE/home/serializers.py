from rest_framework import serializers

from home.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow


class MainWheelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainWheel
        fields = ("id","img","name","trackid")

class MainNavSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainNav
        fields = ("id","img","name","trackid")

class MainMustBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainMustBuy
        fields = ("id","img","name","trackid")

class MainShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainShop
        fields = ("id","img","name","trackid")

class MainShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainShow
        fields = ("id","img","name","trackid","categoryid","brandname",
                  "img1","childcid1","productid1","longname1","price1","marketprice1",
                  "img2","childcid2","productid2","longname2","price2","marketprice2",
                  "img3","childcid3","productid3","longname3","price3","marketprice3")