
from rest_framework import serializers

from orders.models import OrderItem

from mountains.models import Equipment

from mountains.models import AdvUser

from orders.models import Order

from mountains.models import Store

from mountains.models import City

from mountains.models import Region

from mountains.models import Delivery

from mountains.models import Payment

from cart.models import Coupon

from mountains.models import Brand






class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvUser
        fields = ('id', 'phone')


# ----------------------------------------------------------------------------------------------------------------------

class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ('type', 'discount', 'is_active')

# ----------------------------------------------------------------------------------------------------------------------


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('payment',)


# ----------------------------------------------------------------------------------------------------------------------


class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = ('delivery_option',)


# ----------------------------------------------------------------------------------------------------------------------


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('title',)


# ----------------------------------------------------------------------------------------------------------------------


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('title',)


# ----------------------------------------------------------------------------------------------------------------------


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('title',)


# ----------------------------------------------------------------------------------------------------------------------


class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = ('id', 'title',)


# ----------------------------------------------------------------------------------------------------------------------


class StoreSerializer(serializers.ModelSerializer):
    equipments = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')

    class Meta:
        model = Store
        fields = ('title', 'address', 'equipments')


# ----------------------------------------------------------------------------------------------------------------------


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # region = RegionSerializer()
    # city = CitySerializer()
    # store = StoreSerializer()
    # delivery = DeliverySerializer()
    # payment = PaymentSerializer()
    # coupon = CouponSerializer()

    class Meta:
        model = Order
        fields = ('user', )


# ----------------------------------------------------------------------------------------------------------------------


class OrderItemSerializer(serializers.ModelSerializer):

    order = OrderSerializer(read_only=True)
    # user = UserSerializer(read_only=True)
    # equipment = EquipmentSerializer(read_only=True)

    def update(self, order_item,  validated_data):
        order_item.id = validated_data.get('id', order_item.id)
        order_item.status = validated_data.get('status', order_item.status)
        return order_item

    class Meta:
        model = OrderItem
        fields = ('id', 'status', 'price', 'order',)
        lookup_field = ('id',)










