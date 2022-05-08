from django.urls import path

from .views import AllOrderItems, AllStoresView, EquipmentView, UpdateOrderItem

app_name ='restapp'

urlpatterns = [
    path('', AllOrderItems.as_view(), name='all_order_items'),
    path('all_stores/', AllStoresView.as_view(), name='all_stores'),
    path('equipments/', EquipmentView.as_view(), name='equipments'),
    path('update/<int:id>/', UpdateOrderItem.as_view(), name='update'),
]