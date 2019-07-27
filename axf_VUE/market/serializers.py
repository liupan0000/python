from rest_framework import serializers

from market.models import Goods, FoodType


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields ="__all__"

class FoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodType
        fields = "__all__"