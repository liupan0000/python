from alipay import AliPay
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from axf_VUE.settings import ALI_APP_ID, ALIPAY_PUBLIC_KEY, APP_PRIVATE_KEY
from cart.authentication import UserTokenAuthentication
from common.status_code import NOT_LOGIN, NOT_SELECT
from order.models import OrderModel, OrderGoods, OrderGoodsInfo
from order.serializers import OrderModelSerializer
from users.models import userModel


class OrdersView(ListCreateAPIView):
    authentication_classes = UserTokenAuthentication,
    def post(self, request, *args, **kwargs):
        if not isinstance(request.user,userModel):
          data = {
              "msg":"not login",
              "status":NOT_LOGIN
          }

          return Response(data)
        if not request.user.cartmodel_set.filter(c_is_select=True).exists():
            data = {
                "msg":"please select goods",
                "status":NOT_SELECT
            }
            return Response(data)

        # 生成订单
        order_obj = OrderModel()
        order_obj.o_user = request.user
        order_obj.o_price=self.cacl_price()
        order_obj.save()

        #订单商品
        carts = request.user.cartmodel_set.filter(c_is_select=True).all()
        for cart_obj in carts:
            order_goods = OrderGoods()
            order_goods.o_goods_num = cart_obj.c_goods_num
            order_goods.o_order = order_obj
            order_goods.save()

            order_goods_info = OrderGoodsInfo()
            order_goods_info.o_goods = order_goods

            order_goods_info.productid = cart_obj.c_goods.productid
            order_goods_info.productimg = cart_obj.c_goods.productimg
            order_goods_info.productname = cart_obj.c_goods.productname
            order_goods_info.productlongname = cart_obj.c_goods.productlongname
            order_goods_info.isxf = cart_obj.c_goods.isxf
            order_goods_info.pmdesc = cart_obj.c_goods.pmdesc
            order_goods_info.specifics = cart_obj.c_goods.specifics
            order_goods_info.price = cart_obj.c_goods.price
            order_goods_info.marketprice = cart_obj.c_goods.marketprice
            order_goods_info.childcid = cart_obj.c_goods.childcid
            order_goods_info.childcidname = cart_obj.c_goods.childcidname
            order_goods_info.dealerid = cart_obj.c_goods.dealerid
            order_goods_info.storenums = cart_obj.c_goods.storenums
            order_goods_info.productnum = cart_obj.c_goods.productnum

            order_goods_info.save()
            # 生成订单后删除购物车中的数据
            cart_obj.delete()

        order_serializer = OrderModelSerializer(order_obj)
        data = {
            "msg": "ok",
            "status": HTTP_201_CREATED,
            "data": order_serializer.data
        }

        return Response(data)

    def cacl_price(self):
        carts = self.request.user.cartmodel_set.filter(c_is_select=True)
        sum = 0
        for cart_obj in carts:
            sum += cart_obj.c_goods_num * cart_obj.c_goods.price
        return sum
@api_view(["GET","POST"])
def alipay_gen(request):
    order_no = request.query_params.get("order_no")

    order_obj = OrderModel.objects.get(pk=order_no)

    alipay = AliPay(
        appid=ALI_APP_ID,
        app_notify_url=None,  # 默认回调url
        app_private_key_string=APP_PRIVATE_KEY,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type="RSA",  # RSA 或者 RSA2
        debug=False  # 默认False
    )

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no="2019061900%d" % order_obj.id,
        total_amount=order_obj.o_price,
        subject=order_obj.ordergoods_set.first().ordergoodsinfo.productlongname,
        return_url="http://localhost:8000/index",
        notify_url="http://localhost:8000/index"  # 可选, 不填则使用默认notify url
    )
    net = "https://openapi.alipaydev.com/gateway.do?"
    data = {
        "msg":'ok',
        "status":200,
        "data":{
            "pay_url":net+order_string
        }
    }
    return JsonResponse(data)