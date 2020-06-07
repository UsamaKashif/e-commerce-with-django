from django.db import models
from django.contrib.auth.models import User

from django.shortcuts import reverse

from PIL import Image
# Create your models here.

class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=300, null=True)

    def __str__(self):
        return self.name

CATEGORY_CHOICE = (
    ("s","Shirt"),
    ("SW","Sport Wear"),
    ("OW","Outwear"),
)

LABEL_CHOICE = (
    ("P","primary"),
    ("S","secondary"),
    ("D","danger"),
)

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=2)
    description = models.TextField(null=True)
    image = models.ImageField(default="default_img.png",upload_to="product_images")

    def __str__(self):
        return self.name

    @property
    def get_brief_decription(self):
        d = int(len(self.description)/5)
        return self.description[:d]
    
    @property
    def get_image_url(self):
        try:
            return self.image.url 
        except:
            return ""

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 250 or img.width > 250:
            outputSize = (250, 250)

            img.thumbnail(outputSize)
            img.save(self.image.path)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL , null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default = False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = 0
        for item in orderitems:
            if item.product.discount_price:
                total += item.get_total_discount_item_price()
            else:
                total += item.get_total_item_price()
        return total

    


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL , null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL , null=True,blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    def get_total_item_price(self):
        return self.quantity * self.product.price
    
    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()


class ShippingAddress (models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL , null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL , null=True,blank=True)
    street = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    apartment = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.street
