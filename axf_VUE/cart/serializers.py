from rest_framework import serializers

from cart.models import CartModel


class CartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartModel
        fields = ("id","c_user","c_goods","c_goods_num","c_is_select")