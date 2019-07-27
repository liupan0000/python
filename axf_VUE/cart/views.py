from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import NotAuthenticated, ParseError, PermissionDenied
from rest_framework.generics import  ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from cart.authentication import UserTokenAuthentication
from cart.models import CartModel
from cart.serializers import CartModelSerializer
from common.status_code import NOT_LOGIN
from users.models import userModel


class CartsView(ListCreateAPIView):

    queryset = CartModel.objects.all()
    serializer_class = CartModelSerializer
    authentication_classes = UserTokenAuthentication,

    def get(self, request, *args, **kwargs):
        if not isinstance(self.request.user,userModel):
            data = {
                "msg":"not login",
                "status":"NOT_LOGIN"
            }
            return Response(data)
        return super().get(request,*args,**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset=queryset.filter(c_user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        if not isinstance(self.request.user,userModel):
            data = {
                "msg":"not login",
                "status":"NOT_LOGIN"
            }
            return Response(data)
        action = request.query_params.get("action")
        if action =="add_to_cart":
            return self.add_to_cart_from_goods(request,*args,**kwargs)
        elif action=="add_to_cart_num":
            return self.add_to_cart_num(request,*args,**kwargs)
        elif action=="sub_to_cart_num":
            return self.sub_to_cart_num(request,*args,**kwargs)
        elif action=="change_cart_status":
            return self.change_cart_status(request,*args,**kwargs)
        elif action=="all_select":
            return self.all_select(request,*args,**kwargs)
        else:
            raise ParseError(detail="please supply correct action")

    def add_to_cart_from_goods(self, request, *args,**kwargs):
        goods_id = request.data.get("goods_id")
        cart_obj = CartModel.objects.filter(c_goods_id=goods_id).filter(c_user=request.user).first()
        if cart_obj:
            cart_obj.c_goods_num = cart_obj.c_goods_num+1
        else:
            cart_obj=CartModel()
            cart_obj.c_user = request.user
            cart_obj.c_goods_id = goods_id
        cart_obj.save()
        data = {
            "msg":"ok",
            "status":HTTP_201_CREATED,
            "data":{
                "c_goods_num":cart_obj.c_goods_num,
                }
            }
        return Response(data)

    def get_cart_object(self):
        cart_id = self.request.data.get("cart_id")
        cart_obj = self.request.user.cartmodel_set.filter(pk=cart_id).first()
        if not cart_obj:
            raise PermissionDenied(detail="not found")
        return cart_obj

    def add_to_cart_num(self, request, *args,**kwargs):
        cart_obj = self.get_cart_object()
        cart_obj.c_goods_num = cart_obj.c_goods_num+1
        cart_obj.save()
        data = {
            'msg':"ok",
            'status':HTTP_201_CREATED,
            "data":{
                "c_goods_num":cart_obj.c_goods_num,
                "total_price":self.cacl_price()
            }
        }
        return Response(data)

    def sub_to_cart_num(self,request,*args,**kwargs):
        cart_obj = self.get_cart_object()
        if cart_obj.c_goods_num==1:
            cart_obj.delete()
            c_goods_num=0
        else:
            cart_obj.c_goods_num=cart_obj.c_goods_num-1
            cart_obj.save()
            c_goods_num = cart_obj.c_goods_num
        data = {
            "msg":"ok",
            "status":HTTP_204_NO_CONTENT,
            "data":{
                "c_goods_num":c_goods_num,
                "total_price":self.cacl_price()
            }
        }
        return Response(data)

    def change_cart_status(self, request, *args,**kwargs):
        cart_obj=self.get_cart_object()
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()
        if not cart_obj.c_is_select:
            is_all_select = False
        else:
            is_all_select = not CartModel.objects.filter(c_user=request.user).filter(c_is_select=False).exists()
        data = {
            "msg":"change success",
            "status":HTTP_201_CREATED,
            "data":{
                "cart_status":cart_obj.c_is_select,
                "is_all_select":is_all_select,
                "total_price":self.cacl_price()
            }
        }
        return Response(data)

    def all_select(self, request, *args,**kwargs):
        if CartModel.objects.filter(c_user=request.user).filter(c_is_select=False).exists():
            carts = request.user.cartmodel_set.filter(c_is_select=False)
            for cart_obj in carts:
                cart_obj.c_is_select = True
                cart_obj.save()
            data = {
                "msg":"ok",
                "status":HTTP_201_CREATED,
                "data":{
                    "result":"全选",
                    "total_price":self.cacl_price()
                }
            }
            return Response(data)
        elif CartModel.objects.filter(c_user=request.user).exists() and not CartModel.objects.filter(c_user=request.user).filter(c_is_select=False).exists():
            carts = request.user.cartmodel_set.filter(c_is_select = True)
            for cart_obj in carts:
                cart_obj.c_is_select = False
                cart_obj.save()
            data = {
                "msg":"ok",
                "status":HTTP_201_CREATED,
                "data":{
                    "result":"反选",
                    "total_price":self.cacl_price()
                }
            }
            return Response(data)

    def cacl_price(self):
        carts = self.request.user.cartmodel_set.filter(c_is_select =True)
        sum = 0
        for cart_obj in carts:
            sum+=cart_obj.c_goods_num*cart_obj.c_goods.price
        return sum










