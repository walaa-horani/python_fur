from django.db import models
from  django.contrib.auth.models import User
from store.models import  Product
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details=models.ManyToManyField(Product, through='OrderDetails')
    is_finished = models.BooleanField()
    total = 0
    items_count = 0

    def __str__(self):
        return  'user ' + self.user.username + 'order_id:' + str(self.id)


class OrderDetails(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity= models.IntegerField()

    def __str__(self):
        return  'user: ' + self.order.user.username + 'product' + self.product.title


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_address = models.CharField(max_length=450) 
    shipment_phone = models.CharField(max_length=20)    
    card_number = CardNumberField(max_length=450) 
    expire = CardExpiryField()
    security_code = SecurityCodeField()       



