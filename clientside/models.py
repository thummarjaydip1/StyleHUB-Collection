from django.db import models
from adminside.models import *
from clientside.models import *
from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    mobile=models.IntegerField()
    subject=models.CharField()
    message=models.TextField()

class Feedback(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    mobile=models.IntegerField()
    rating=models.CharField()
    message=models.TextField()


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200, default="Unknown Product")
    size = models.CharField(max_length=10, default="M")  # <-- Add this
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"{self.product_name} ({self.size}) - {self.mobile}"
