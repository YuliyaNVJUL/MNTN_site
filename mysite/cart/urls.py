from django.urls import path
from . import views
from .views import coupon_apply

app_name = 'cart'
urlpatterns = [
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('add/<equipment_id>/', views.cart_add, name='cart_add'),
    path('remove/<equipment_id>/', views.cart_remove, name='cart_remove'),
    path('coupon/', coupon_apply, name='coupon_apply'),
]