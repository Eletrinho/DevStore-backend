from django.db import models
from django.db.models.signals import m2m_changed


class CartManager(models.Manager):

    def create_cart(self, user=None):
        user_obj = None
        if user:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        cart_obj = self.model.objects.filter(id=cart_id).first()
        if cart_obj is not None:
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = self.create_cart(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj 

class Cart(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def get_total_price(self):
        return sum([item.get_total_price() for item in self.items.all()])
        
    def __str__(self):
        return f"Cart of {self.user.email if self.user.email else 'Anonymous'} - Created at {self.created_at}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"