from django.contrib import admin
from .models import Category,Dish,Customer,Order,OrderContent,Staff,Data,DeliveryBoy,Cart
# Register your models here.
admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderContent)
admin.site.register(Staff)
admin.site.register(Data)
admin.site.register(DeliveryBoy)
admin.site.register(Cart)
