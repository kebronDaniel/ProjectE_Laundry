from django.db import models
from django.conf import settings

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

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        self.user.username


