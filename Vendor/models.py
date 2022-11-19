from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from asgiref.sync import async_to_sync 
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/%Y/%m/%d")
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='dishes/%Y/%m/%d')
    details = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    sale_price = models.FloatField(default=price)
    discount = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    num_order = models.IntegerField(default=0)

    def __str__(self):
        return self.name 
    
    def calculateSalePrice(self):
       self.sale_price = (100.0 - self.discount)/100.0 * self.price


class Customer(models.Model):
    pending = 'Pending'
    verified = 'Verified'

    STATUS = (
        (pending,pending),
        (verified,verified),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    contact = models.CharField(max_length = 10)
    orders = models.IntegerField(default=0)
    total_sale = models.IntegerField(default=0)

    def __str__(self):
        return self.customer.username #return self.customer.first_name + " " + self.customer.last_name

class Staff(models.Model):
    admin = 'Admin'
    deliveryboy = 'Delivery Boy'
    chef = 'Chef'

    ROLES = (
        (admin,admin),
        (chef,chef),
        (deliveryboy,deliveryboy),
    )
    
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    contact = models.CharField(max_length = 10)
    email = User.email
    salary = models.IntegerField()
    role = models.CharField(max_length = 30, choices = ROLES)
    
    def __str__(self):
        return self.staff_id.first_name + " " + self.staff_id.last_name

class Order(models.Model):
    pending = 'Pending'
    completed = 'Completed'

    STATUS = (
        (pending,pending),
        (completed,completed),
    )

    cod = 'Cash On Delivery'
    card = 'Card Payment'
    upi = 'UPI Payment'

    PAYMENT = (
        (cod,cod),
        (card,card),
        (upi,upi),
    )

    pickup = 'PickUp'
    delivery = 'Delivery'

    TYPE = (
        (pickup, pickup),
        (delivery, delivery),
    )

    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_timestamp = models.CharField(max_length=100, blank=True)
    delivery_timestamp = models.CharField(max_length=100, blank=True)
    payment_status = models.CharField(max_length = 100, choices = STATUS)
    delivery_status = models.CharField(max_length = 100, choices = STATUS)
    if_cancelled = models.BooleanField(default = False)
    total_amount = models.IntegerField()
    payment_method = models.CharField(max_length = 100, choices = PAYMENT)
    location = models.CharField(max_length=200, blank=True, null=True)
    delivery_boy = models.ForeignKey(Staff,on_delete=models.CASCADE, null=True, blank=True)
    
    def confirmOrder(self):
        self.order_timestamp = timezone.localtime().__str__()[:19]
        self.payment_status = self.completed
        self.save()

    def confirmDelivery(self):
        self.delivery_timestamp = timezone.localtime().__str__()[:19]
        self.delivery_status = self.completed
        self.save()
    
    def __str__(self):
        return self.customer.__str__()

class Comment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)

class Data(models.Model):
    date = models.DateField()
    sales = models.IntegerField()
    expenses = models.IntegerField()

class OrderContent(models.Model):
    quantity = models.IntegerField(default=1)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Cart(models.Model):
    quantity = models.IntegerField(default=1)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class DeliveryBoy(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_boy = models.ForeignKey(Staff, on_delete=models.CASCADE)







