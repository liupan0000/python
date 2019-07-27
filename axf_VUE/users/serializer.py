from rest_framework import serializers

from users.models import userModel


class userSerializer(serializers.ModelSerializer):

    class Meta:

        model = userModel

        fields = ("id","u_name","u_password","u_email","u_icon","is_delete","is_active")
