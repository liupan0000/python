from django.db import models

# Create your models here.
from django.db.models import Q
from rest_framework.exceptions import NotFound


class userModel(models.Model):

    u_name= models.CharField(max_length=32,unique=True,null=False,blank=False)

    u_password = models.CharField(max_length=256)

    u_email = models.CharField(max_length=32,unique=True,null=False,blank=False)

    u_icon = models.CharField(max_length=256,null=True,blank=True,default=" ")

    is_delete = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    class Meta:

        db_table = "user_model"

    @classmethod

    def check_username(cls,u_name):

        return userModel.objects.filter(u_name=u_name)

    @classmethod

    def check_email(cls,u_email):

        return userModel.objects.filter(u_email=u_email)

    @classmethod

    def get_user(cls,u_user):

        user = userModel.objects.filter(Q(u_name=u_user) | Q(u_email=u_user)).first()

        if not user:

            raise NotFound(detail="用户不存在")

        return user

    def check_password(self,u_password):

        return self.u_password==u_password

    # @classmethod
    # def user_modify_password(cls, u_user):
    #     user = userModel.objects.filter(Q(u_name=u_user) & Q(u_email=u_user)).first()
    #     return user









