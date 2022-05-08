from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .cart import Cart
from mountains.models import Equipment
from .forms import CartAddEquipmentForm, CouponForm
from .models import Coupon




@require_POST
def cart_add(request, equipment_id):
    cart = Cart(request)
    equipment = get_object_or_404(Equipment, id=equipment_id)
    form = CartAddEquipmentForm(request.POST)
    if form.is_valid():
        if equipment.available == 'On sale soon' or equipment.available == 'Wkrotce na wyprzedazy':
            raise ValidationError('Equipment in not available yet!')
        cd = form.cleaned_data
        cart.add(equipment=equipment, quantity=cd['quantity'], update_quantity=cd['update'])
        # print(cart.__dict__)
    return redirect('cart:cart_detail')


def cart_remove(request, equipment_id):
    cart = Cart(request)
    equipment = get_object_or_404(Equipment, id=equipment_id)
    cart.remove(equipment)
    return redirect('cart:cart_detail')



def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddEquipmentForm(
            initial={'quantity': item['quantity'], 'update': True})
    coupon_form = CouponForm()
    context = {"cart": cart, "coupon_form": coupon_form}
    return render(request, 'cart_detail.html', context)




def coupon_apply(request):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code=code,
                                          start__lte=now,
                                          end__gte=now,
                                          is_active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
        return redirect('cart:cart_detail')
