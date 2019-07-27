from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from market.models import Goods, FoodType
from market.serializers import GoodsSerializer, FoodTypeSerializer

ALL_TYPES = '0'
ORDER_DEFAULT = '0'
ORDER_PRICE_UP="1"
ORDER_PRICE_DOWN="2"
ORDER_SALE_DOWN='3'

class GoodsView(ListAPIView):
    serializer_class = GoodsSerializer
    queryset = Goods.objects.all()
    # 筛选
    def get_queryset(self):
        queryset = super().get_queryset()
        categoryid = self.request.query_params.get("typeid","104749")
        queryset = queryset.filter(categoryid=categoryid)
        childcid = self.request.query_params.get("childcid","0")
        if childcid !=ALL_TYPES:
            queryset = queryset.filter(childcid=childcid)

        #  排序
        order_by = self.request.query_params.get("order_by","0")
        if order_by==ORDER_PRICE_UP:
            queryset=queryset.order_by("price")
        elif order_by==ORDER_PRICE_DOWN:
            queryset=queryset.order_by("-price")
        elif order_by==ORDER_SALE_DOWN:
            queryset=queryset.order_by("-productnum")

        return queryset
    #
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        typeid = self.request.query_params.get('typeid',"104749")
        foodtype = FoodType.objects.get(typeid=typeid)
        foodtypechildtypenames = foodtype.childtypenames
        foodtypechildname_list = foodtypechildtypenames.split("#")
        foodtype_childname_list=[]
        for foodtypechildtypename in foodtypechildname_list:
            foodtype_childname = dict()
            foodtype_childname_split = foodtypechildtypename.split(":")
            foodtype_childname['child_name'] = foodtype_childname_split[0]
            foodtype_childname['child_value'] = foodtype_childname_split[1]
            foodtype_childname_list.append(foodtype_childname)

        order_rule_list =[
            {
                "order_name": "综合排序",
                "order_value":ORDER_DEFAULT
            },
            {
                "order_name":"价格升序",
                "order_value":ORDER_PRICE_UP
            },
            {
                "order_name":"价格降序",
                "order_value":ORDER_PRICE_DOWN
            },
            {
                "order_name":"销量降序",
                "order_value":ORDER_SALE_DOWN
            },
        ]
        data = {
            "data":{
                "order_rule_list":order_rule_list,
                "goods_list":serializer.data,
                "foodtype_childname_list":foodtype_childname_list,
            }
        }
        return Response(data)

class FoodTypesView(ListAPIView):
    serializer_class = FoodTypeSerializer
    queryset = FoodType.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "msg": "ok",
            "status": 200,
            "data": serializer.data
        }
        return Response(data)
