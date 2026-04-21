from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.cart import Cart
from decimal import Decimal


@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name', request.user.first_name),
            last_name=request.POST.get('last_name', request.user.last_name),
            email=request.POST.get('email', request.user.email),
            phone=request.POST.get('phone', request.user.phone or ''),
            address=request.POST.get('address', request.user.address or ''),
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['discount_price'],
                quantity=item['quantity'],
            )
        order.update_total()
        cart.clear()
        return redirect('orders:order_success')

    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'breadcrumbs': [
            {'title': 'Главная', 'url': '/'},
            {'title': 'Корзина', 'url': '/cart/'},
            {'title': 'Оформление заказа', 'url': ''},
        ],
    })


@login_required
def order_success(request):
    return render(request, 'orders/order_create.html', {
        'success': True,
        'breadcrumbs': [
            {'title': 'Главная', 'url': '/'},
            {'title': 'Заказ оформлен', 'url': ''},
        ],
    })