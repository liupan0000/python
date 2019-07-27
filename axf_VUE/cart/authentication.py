from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication


class UserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.query_params.get("token")
            user =cache.get(token)
            return user,token
        except Exception as e:
            print(e)
            print("认证成功")