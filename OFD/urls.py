"""OFD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from Vendor import views
urlpatterns = [

    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('about/',views.about,name="about"),
    path('menu/',views.menu,name="menu"),
    path('menu/search',views.menusearch,name="menusearch"),
    path('menu/details/<int:mid>',views.detailview,name="detail"),
    path('cart/', views.cart, name='cart'),
    path('addTocart/(?P<foodID>\d+)/(?P<userID>\d+)/', views.addTocart, name='addTocart'),
    path('delete_item/(?P<ID>\d+)/', views.delete_item, name='delete_item'),
    #Authentication
    path('register/',views.signup,name="register"),
    path('accounts/login/',views.loginpage,name='login'),
    path('logout/', views.logoutpage, name='logout'),
    #admin funcs
    path('dashboard/admin/users/', views.users_admin, name='users_admin'),
    path('dashboard/admin/orders/', views.orders_admin, name='orders_admin'),
    path('dashboard/admin/orders/details/(?P<ID>\d+)/',views.ordercontent_admin,name='orders_details'),
    path('dashboard/admin/foods/', views.dishes_admin, name='foods_admin'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard'),
    path('dashboard/admin/sales/', views.sales_admin, name='sales_admin'),


    path('dashboard/admin/foods/add_food/$', views.add_food, name='add_food'),
    path('dashboard/admin/foods/editFood/(?P<foodID>\d+)/$', views.edit_food, name='edit_food'),
    

    path('dashboard/admin/orders/confirm_order/(?P<orderID>\d+)/$', views.confirm_order, name='confirm_order'),
    path('dashboard/admin/orders/confirm_delivery/(?P<orderID>\d+)/$', views.confirm_delivery, name='confirm_delivery'),




    #ORDers place and myorders
    path('placeOrder/', views.placeOrder, name='placeOrder'),
    #Customer profile
    path('profile/',views.cust_profile,name="profile"),
    path('profile/user',views.user_profile,name="userp"),
    path('myorders/', views.my_orders, name='my_orders'),

]+static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
