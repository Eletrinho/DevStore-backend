import uuid
from django.db import models

ORDER_STATUS = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('canceled', 'Canceled'),
)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(
        'users.Address', on_delete=models.CASCADE, related_name='orders')

    status = models.CharField(
        max_length=16, choices=ORDER_STATUS, default='created')

    shipping_price = models.DecimalField(
        default=10.00, max_digits=10, decimal_places=2)
    total_price = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def update_total_price(self):
        total = self.cart.get_total_price() + self.shipping_price
        Order.objects.filter(pk=self.pk).update(total_price=total)

    def __str__(self):
        return f"Order {self.id} - {self.order_status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"
