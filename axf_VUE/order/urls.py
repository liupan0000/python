from django.conf.urls import url

from order import views

urlpatterns = [
    url(r'^alipay/',views.alipay_gen),
    url(r'',views.OrdersView.as_view())
]