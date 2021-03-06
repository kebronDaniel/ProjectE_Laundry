from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from phone_field import PhoneField

CATEGORY_CHIOCES = (
    ('SU', 'Suit'),
    ('SH', 'Shirt'),
    ('TR', 'Trouser'),
    ('HS', 'HomeSheet'),
    ('JK', 'Jacket')
)
LABEL_CHIOCES = (
    ('P', 'Primary'),
    ('S', 'Secondary'),
    ('D', 'Danger')
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHIOCES, max_length=2)
    label = models.CharField(choices=LABEL_CHIOCES, max_length=1)
    slug = models.SlugField()
    description = models.TextField(default="This is the description of this product")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("item", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

    def __str__(self):
        return self.user.username

class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=200)
    unique_name = models.CharField(max_length=200)
    phone = PhoneField(default = 0000)

    def __str__(self):
        return self.user.username


