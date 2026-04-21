from decimal import Decimal
from catalog.models import Product
from decimal import Decimal

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'discount_percent': product.discount_percent,
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            if item['discount_percent'] > 0:
                item['discount_price'] = item['price'] * (1 - item['discount_percent'] / 100)
            else:
                item['discount_price'] = item['price']
            item['total_price'] = item['discount_price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * (Decimal('1') - Decimal(item['discount_percent']) / Decimal('100')) * item[
                'quantity']
            for item in self.cart.values()
        )

    def clear(self):
        del self.session['cart']
        self.save()