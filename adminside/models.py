from django.db import models

class Adminlogin(models.Model):
    username=models.CharField()
    password=models.TextField()

class Product(models.Model):
    name=models.CharField()
    category=models.CharField()
    type=models.CharField()
    price=models.FloatField()
    image = models.ImageField(upload_to='', null=True, blank=True)