from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from rest_framework import status
from rest_framework.exceptions import NotAcceptable, AuthenticationFailed, ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from axf_VUE.settings import USER_TOKEN_TIMEOUT, ACTIVATE_TIME, SERVER_HOST, EMAIL_HOST_USER,MODIFY_TIME
from common.token import generate_token, get_code
from users.models import userModel
from users.serializer import userSerializer
from users.tasks import send_code, send_email_asy


class usersView(CreateAPIView):

    queryset = userModel.objects.all()

    serializer_class = userSerializer

    def get(self,request,*args,**kwargs):

        action = request.query_params.get("action")

        if action =="activate":

            try:

                token=request.query_params.get("token")

                u_name = cache.get(token)

                if u_name:

                    cache.delete(token)

                user = userModel.get_user(u_name)

                user.is_active = True

                user.save()

                # request.session["info"] = "激活成功"

                messages.warning(request._request,"激活成功")

            except Exception as e:

                print(e)

                # request.session["info"] = "激活失败"

                messages.warning(request._request,"激活失败")

            return redirect("/index/")

        # if action == "modify":
        #
        #     try:
        #
        #         token = request.query_params.get("token")
        #
        #         u_password = cache.get(token)
        #
        #         if u_password:
        #             cache.delete(token)
        #
        #         user = userModel.get_user(u_password)
        #
        #         user.save()
        #
        #         # request.session["info"] = "激活成功"
        #
        #         messages.warning(request._request, "密码修改成功")
        #
        #     except Exception as e:
        #
        #         print(e)
        #
        #         # request.session["info"] = "激活失败"
        #
        #         messages.warning(request._request, "密码修改失败")
        #
        #     return redirect("/login/")

    #     if action == "re_login":
    #         return self.re_login(request, *args, **kwargs)
    #
    # def re_login(self, request, *args, **kwargs):
    #     try:
    #         u_name = request.data.get('u_name')
    #         u_email = request.data.get('u_email')
    #         re_password = request.data.get('re_password')
    #         user = userModel.user_modify_password(u_name, u_email)
    #         user.u_password = re_password
    #         user.save()
    #         data = {
    #             'status': status.HTTP_205_RESET_CONTENT,
    #             'msg': 'Password update success'
    #         }
    #         return Response(data)
    #     except Exception as e:
    #         raise ValidationError(detail='Password update failed')

    def post(self,request,*args,**kwargs):
        print('a')

        action = request.query_params.get("action")

        if action=="register":

            return self.do_register(request,*args,**kwargs)

        elif action=="login":

            return self.do_login(request,*args,**kwargs)

        elif action=="check_username":

            return self.check_user_name(request,*args,**kwargs)

        elif action=="check_email":

            return self.check_user_email(request,*args,**kwargs)
        # elif action=="modify_password":
        #     return self.modify_password(request,*args,**kwargs)

        elif action=="modify_info":

            pass

        elif action=="modify_icon":

            pass

        elif action=="get_info":
            pass
        #
        # elif action=="update_password":
        #     return self.do_update_password(request,*args,**kwargs)

        elif action=="test_asy":
            send_code.delay()
            return Response({"msg":"success"})

        else:

            raise NotAcceptable(detail="请提供正确的动作")

    def do_register(self,request,*args,**kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        u_email = serializer.data.get("u_email")

        u_name = serializer.data.get("u_name")

        subject = "axf用户激活邮件"

        activate_email = loader.get_template("activate.html")

        token =generate_token()

        cache.set(token,u_name,timeout = ACTIVATE_TIME)

        activate_url = SERVER_HOST + "/user/?action=activate&token=" + token

        html_msg = activate_email.render({"u_name":u_name,"activate_url":activate_url})
        send_email_asy.delay(u_email,subject,html_msg)

        data = {

            "msg":"创建成功",
            "status":HTTP_201_CREATED,
            "data":serializer.data
        }

        return Response(data,HTTP_201_CREATED, headers=headers)


    def do_login(self,request,*args,**kwargs):

        u_user = request.data.get("u_user")

        u_password = request.data.get("u_password")

        user = userModel.get_user(u_user)

        if not user.check_password(u_password):

            raise AuthenticationFailed(detail="密码错误")

        token = generate_token()

        cache.set(token,user,timeout=USER_TOKEN_TIMEOUT)

        data = {

            "msg":"login success",
            "status":HTTP_200_OK,
            "token":token
        }

        return Response(data)

    # 用户名预校验

    def check_user_name(self,request,*args,**kwargs):

        u_name = request.data.get("u_name")

        if userModel.check_username(u_name):

            raise ValidationError(detail="用户名已存在")

        data ={

            "satus":HTTP_200_OK,
            "mag":"用户名可用"
        }

        return Response(data)

    # 邮箱预校验
    def check_user_email(self,request,*args,**kwargs):

        u_email = request.data.get("u_email")

        if userModel.check_email(u_email):

            raise ValidationError(detail="邮箱已存在")

        data = {

            "status":HTTP_200_OK,
            "msg":"邮箱可以使用"
        }

        return Response(data)
    #
    # def do_update_password(self, request, *args, **kwargs):
    #     u_name = request.data.get('u_name')
    #     u_email = request.data.get('u_email')
    #     try:
    #         user = userModel.user_modify_password(u_name, u_email)
    #         token = generate_token()
    #         cache.set(token, user, timeout=UPDATE_TOKEN_TIMAOUT)
    #         code = get_code()
    #         subject = 'AXF验证码'
    #         msg = 'You are modifying the password.' \
    #               'If you do not operate by yourself, please check the security of the account ' \
    #               '\n Verification code is ' + code + '' \
    #                                                   '\n And the token to modify password ' + token
    #
    #         send_mail(subject=subject, message=msg, from_email=EMAIL_HOST_USER, recipient_list=(u_email,))
    #         data = {
    #             'status': HTTP_200_OK,
    #             'msg': 'The verification code has been sent to your mailbox',
    #         }
    #         request.session['code'] = code
    #         return Response(data)
    #     except Exception as e:
    #         raise ValidationError('')
    #
    # def put(self, request, *args, **kwargs):
    #     code = request.data.get('code')
    #     if code != request.session.get('code'):
    #         raise NotAcceptable(detail='Verification code error')
    #     try:
    #         token = request.data.get('token')
    #         re_password = request.data.get('re_password')
    #         user = cache.get(token)
    #         user.u_password = re_password
    #         user.save()
    #         data = {
    #             'status': status.HTTP_200_OK,
    #             'msg': 'Password update success'
    #         }
    #         return Response(data)
    #     except Exception as e:
    #         raise ValidationError(detail='Password update success')
    #
    # def modify_password(self,request,*args,**kwargs):
    #
    #     u_email = request.data.get("u_email")
    #
    #     u_name = request.data.get("u_name")
    #
    #     if u_name and u_email:
    #
    #         subject = "axf用户修改密码邮件"
    #
    #         msg = "修改成功"
    #
    #         modify_email = loader.get_template("modify.html")
    #
    #         token = generate_token()
    #
    #         cache.set(token, u_name, timeout=MODIFY_TIME)
    #
    #         modify_url = SERVER_HOST + "/user/?action=modify_password&token=" + token
    #
    #         html_msg = modify_email.render({"u_name": u_name, "modify_url": modify_url})
    #         send_mail(subject=subject, message=msg, from_email=EMAIL_HOST_USER, recipient_list=(u_email,),
    #               html_message=html_msg)


