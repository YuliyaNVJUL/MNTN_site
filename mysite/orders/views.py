from django.shortcuts import render
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from mountains.models import Delivery
from mountains.models import Payment
from mountains.models import Equipment
from mountains.models import Store




def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm()
    payments = Payment.objects.all()
    deliveries = Delivery.objects.all()
    stores = Store.objects.all()
    context = {"cart": cart, "form": form, 'payments': payments, "deliveries":  deliveries, "stores": stores}
    if request.method == 'POST':

        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            delivery = Delivery.objects.get(id=request.POST.get('del'))
            store = Store.objects.get(id=request.POST.get('stor'))
            payment = Payment.objects.get(id=request.POST.get('pay'))

            order.delivery = delivery
            order.payment = payment
            order.store = store
            order.save()

            for item in cart:
                OrderItem.objects.create(
                                         order=order,
                                         equipment=item['equipment'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            for i in cart:
                number = i['quantity']
                cart_equipment = i['equipment']
                equipments = Equipment.objects.filter(pk=cart_equipment.id)
                for equipment in equipments:
                    equipment.remainder -= number
                    equipment.save()
                    if equipment.remainder == 0:
                        Equipment.objects.filter(pk=cart_equipment.id).update(available='On order')

            cart.clear()

            return render(request, 'created.html', {'order': order})
        else:
            error = form.errors
            context = {"form": form, "error": error}
    else:
        form = OrderCreateForm

    return render(request, 'create.html', context)