from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from orders.models import OrderItem
from .serializers import OrderItemSerializer, StoreSerializer, RegionSerializer, EquipmentSerializer
from mountains.models import Store
from mountains.models import Equipment




class AllOrderItems(APIView):

    def get(self, request, format=None):
        order_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)




class AllStoresView(APIView):
    def get(self, request):
        stores = Store.objects.prefetch_related('equipments')
        serializer = StoreSerializer(stores, many=True)
        return Response( serializer.data)



class UpdateOrderItem(generics.UpdateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    lookup_field = 'id'

    def get(self, request, id, format=None):
        order_item = OrderItem.objects.get(pk=id)
        serializer = self.get_serializer(order_item)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = request.data.get("status")
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            instance.save()
            return Response(serializer.data)


class EquipmentView(APIView):
    def get(self, request, format=None):
        equipments = Equipment.objects.all()
        serializer = EquipmentSerializer(equipments, read_only=True, many=True)
        return Response(serializer.data)


@receiver(post_save, sender=OrderItem)
def new_order_signal(sender, **kwargs):
    print('Ok')


