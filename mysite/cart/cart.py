from decimal import Decimal
from django.conf import settings
from mountains.models import Equipment

from .models import Coupon


class Cart(object):
    def __init__(self, request):
        """Инициализация корзины"""
        self.session = request.session
        # print(self.session.keys())
        # print(self.session.items())
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
            # print(self.session.items())
        self.cart = cart
        # print(self.cart)
        """инициализация купона из тукещей сессии и сохранение текущего примененного купона"""
        self.coupon_id = self.session.get('coupon_id')


    def add(self, equipment, quantity=1, update_quantity=False):
        """Добавить продукт в корзину или обновить его колличество"""
        if equipment.available != 'On sale soon' and equipment.available != 'Wkrotce na wyprzedazy':
            equipment_id = str(equipment.id)
            if equipment_id not in self.cart:
                self.cart[equipment_id] = {'quantity': 0, "price": str(equipment.price), 'discount': str(equipment.discount)}
                for item in self.cart.values():
                    if equipment.discount:
                        item['price'] = float(equipment.get_discount)
                    else:
                        item['price'] = float(item['price'])

            if update_quantity:
                self.cart[equipment_id]['quantity'] = quantity

            else:
                self.cart[equipment_id]['quantity'] += quantity
                # print(self.cart.items())
            self.save()


    def save(self):
        """Обновление сессии cart"""
        self.session[settings.CART_SESSION_ID] = self.cart

        """Отметить сеанс как обновленныйб чтобы убедиться, что он сохранен"""
        self.session.modified = True


    def remove(self, equipment):
        """Удаление товара из корзины"""
        equipment_id = str(equipment.id)
        if equipment_id in self.cart:
            del self.cart[equipment_id]
            self.save()


    def __iter__(self):
        """Перебор элеметнов в корзине и получение товаров из БД"""
        equipment_ids = self.cart.keys()
        # print(self.cart.values())
        # получение обьектов и добавление их в корзину
        equipments = Equipment.objects.filter(id__in=equipment_ids)
        for equipment in equipments:
            self.cart[str(equipment.id)]['equipment'] = equipment


        for item in self.cart.values():
            # print(item['price'])
            item['price'] = Decimal(item['price'])
            # print(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item



    def __len__(self):
        """Подсчет всех товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())


    def get_total_price(self):
        """Подсчет стоимости товаров в корзине"""

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Удаление корзины из сессии"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            if self.coupon.type == 'Percents':
                return (self.coupon.discount / Decimal('100')) * self.get_total_price()
            else:
                return self.coupon.discount
        return Decimal('0')

    def get_price_discount(self):
        return self.get_total_price() - self.get_discount()

