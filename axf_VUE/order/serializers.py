from rest_framework import serializers

from order.models import OrderModel


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ("id","o_user","o_price","o_ordered_time",'o_status')