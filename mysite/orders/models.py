from decimal import Decimal

from django.db import models

from mountains.models import Region

from mountains.models import City

from mountains.models import Equipment

from mountains.models import Delivery

from mountains.models import Payment

from mountains.models import AdvUser

from mountains.models import Store

from cart.models import Coupon




class Order(models.Model):
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField( max_length=250)
    postal_code = models.CharField(max_length=20)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField( auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    paid = models.BooleanField( default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Order {}'.format(self.id)


    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))




order_item_choises = [
    ("New", "New"),
    ("Processed", "Processed"),
    ("Postponed", "Postponed"),
    ("Refusal", "Refusal"),
    ("Confirmed", "Confirmed"),

]

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='order_items', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=order_item_choises, default='New')
    comments = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity