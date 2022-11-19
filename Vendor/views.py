from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
import json 
import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.sites.shortcuts import get_current_site
#from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
#from reportlab.pdfgen import canvas
from .models import Customer, Comment, Order, Data, Cart, OrderContent, Staff, DeliveryBoy,Category,Dish
from .forms import SignUpForm
# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.email = form.cleaned_data['email']
            user.username = user.email.split('@')[0]
            user.set_password(form.cleaned_data['password'])
            user.save()
            address = form.cleaned_data['address']
            contact = form.cleaned_data['contact']
            customer = Customer.objects.create(customer=user, address=address, contact=contact)
            customer.save()
            return redirect('login')
        
    else:
        form = SignUpForm()
        
    return render(request, 'accounts/register.html', {'form': form})



def loginpage(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request, username= username, password=password)
        if(user is not None):
            login(request,user)
            if user.is_superuser or user.is_staff:
                return HttpResponseRedirect('/admin')
            return redirect('index')
        else:
            messages.info(request,'Username or password is incorrect')
            return render(request,'accounts/login.html')
    return render(request,'accounts/login.html')

def logoutpage(request):
    logout(request)
    return redirect('/accounts/login')
def index(request):
    context={}
    cats = Category.objects.all().order_by('name')
    context['categories'] = cats
    dishes = []
    for cat in cats:
        dishes.append({
            'cat_id':cat.id,
            'cat_name':cat.name,
            'cat_img':cat.image,
            'items':list(cat.dish_set.all().values())
        })
    context['menu'] = dishes
    #delete code
    
    cont = OrderContent.objects.all().order_by('order')
    beh ={}
    print(request.user)
    beh[request.user]={}
    for ct in cont:
        beh[request.user][ct.dish] = 0 
    for ct in cont:
        beh[request.user][ct.dish] += ct.quantity
    print(beh)
    #delete code
    return render(request,'restaurant/index.html',context)

def about(request):
    return render(request,'restaurant/about.html')

def menu(request):
    context={}
    dishes = Dish.objects.all()
       
    if "q" in request.GET:
        id = request.GET.get("q")
        dishes = Dish.objects.filter(category__id=id)
        context['dish_category'] = Category.objects.get(id=id).name 
    
    context['dishes'] = dishes
    return render(request,'restaurant/menu.html',context)

def menusearch(request):
    query = request.GET.get("q")
    dishes = Dish.objects.filter(
        Q(name__contains=query) |
        Q(price__contains=query) |
        Q(category__name__contains=query) 
    )

    context={
        'dishes':dishes   }

    return render(request,'restaurant/menu.html',context)

def detailview(request,mid):
    dish =  Dish.objects.filter(id=mid)
    print(dish)

    return render(request,'restaurant/detail.html',{'dish':dish[0]})

#admin functionalities 
@login_required
@staff_member_required
def dashboard_admin(request):
    comments = Comment.objects.count()
    orders = Order.objects.count()
    customers = Customer.objects.count()
    completed_orders = Order.objects.filter(payment_status="Completed")
    top_customers = Customer.objects.filter().order_by('-total_sale')
    latest_orders = Order.objects.filter().order_by('-order_timestamp')
    datas = Data.objects.filter().order_by('date')
    sales = 0
    for order in completed_orders:
        sales += order.total_amount

    context = {
        'comments':comments,
        'orders':orders,
        'customers':customers,
        'sales':sales,
        'top_customers': top_customers,
        'latest_orders':latest_orders,
        'datas':datas,
    }
    return render(request, 'admin_temp/index.html', context)

@login_required
@staff_member_required
def users_admin(request):
    customers = Customer.objects.filter()
    print(customers)
    return render(request, 'admin_temp/users.html', {'users':customers})

@login_required
@staff_member_required
def orders_admin(request):
    orders = Order.objects.filter()
    print(orders)
    dBoys = Staff.objects.filter(role='Delivery Boy')
    print(dBoys)
    return render(request, 'admin_temp/orders.html', {'orders':orders, 'dBoys':dBoys})

@login_required
@staff_member_required
def ordercontent_admin(request,ID):
    orders = Order.objects.get(id=ID)
    print(orders)
    ordercontent = OrderContent.objects.filter(order=orders)
    dBoys = Staff.objects.filter(role='Delivery Boy')
    print(dBoys)
    return render(request, 'admin_temp/ordercontent.html', {'orders':ordercontent, 'dBoys':dBoys,'ord':orders})
@login_required
@staff_member_required
def dishes_admin(request):
    dishes = Dish.objects.filter()
    return render(request, 'admin_temp/foods.html', {'foods':dishes})

@login_required
@staff_member_required
def sales_admin(request):
    sales = Data.objects.filter()
    return render(request, 'admin_temp/sales.html', {'sales':sales})

@login_required
@staff_member_required
def edit_food(request, foodID):
    food = Dish.objects.filter(id=foodID)[0]
    print(food)
    if request.method == "POST":
        if request.POST['base_price'] != "" and request.POST['base_price'] >=str(0):
            food.price = request.POST['base_price']
        else:
            messages.info(request,'Username or password is incorrect')
        if request.POST['discount'] != "":
            print(type(request.POST['discount']))
            food.discount = request.POST['discount'] 
        else:
            messages.info(request,'Username or password is incorrect')
        
        food.sale_price = (100 - float(food.discount))*float(food.price)/100

        status = request.POST.get('disabled')
        print(status)
        if status == 'on':
            food.is_available = False
        else:
            food.is_available = True
        
        food.save()
        to_email=[]
        cust=user_behaviour(request,food)
        for cus in cust:
            mail_subject = 'Ultimate Offer '
            to = [str(cus.email)]
            to_email.append(to)
            from_email = 'abhinavparakh19@gmail.com'
            message = "Hi "+cus.first_name+" Order Now your favourite dish " + food.name +" now has a discount of "+ str(food.discount)+"%"
            send_mail(
                    mail_subject,
                    message,
                    from_email,
                    to,
                )
    return redirect('foods_admin')


@login_required
@staff_member_required
def add_food(request):
    if request.method == "POST":
        name = request.POST['name']
        course = request.POST['course']
        status = request.POST['status']
        content = request.POST['content']
        base_price = request.POST['base_price']
        discount = request.POST['discount']
        sale_price = (100 - float(discount)) * float(base_price) / 100
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)

        if (name == "") or (course is None) or (status is None) or (content == "") or (base_price == "") or (discount == ""):
            foods = Dish.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'admin_temp/foods.html', {'foods': foods, 'error_msg': error_msg})
        if status == 'Enabled':
            bool_stat = True 
        else:
            bool_stat = False
        cat = Category.objects.filter()
        #print(cat,type(cat))
        for k in cat:
            if course == k.name:
                sup_cat = k
                #print(sup_cat.name,course,type(sup_cat.name),type(course))
        food = Dish.objects.create(name=name, category=sup_cat, is_available=bool_stat, details=content, price=base_price, discount=discount, sale_price=sale_price, image=filename)
        food.save()
        foods = Dish.objects.filter()
        success_msg = "Please enter valid details"
        cust = Customer.objects.all()
        for cus in cust:
            mail_subject ="Checkout a dazzling dish is now available order now !"
            to = [User.objects.get(customer__id=cus.id).email]
            from_email = 'abhinavparakh19@gmail.com'
            message = "Hi "+User.objects.get(customer=cus).first_name+ food.name +"is now available for ordering online dont miss out to taste our newest dish order now "+"Bon appetite"
            send_mail(
                    mail_subject,
                    message,
                    from_email,
                    to,
                )
        return render(request, 'admin_temp/foods.html', {'foods': foods, 'success_msg': success_msg})
        
    return redirect('foods_admin')

@login_required
@staff_member_required
def confirm_order(request, orderID):
    order = Order.objects.get(id=orderID)
    order.confirmOrder()
    order.save()
    customerID = order.customer.id
    customer = Customer.objects.get(id=customerID)
    customer.total_sale += order.total_amount
    customer.orders += 1
    customer.save()
    return redirect('orders_admin')

@login_required
@staff_member_required
def confirm_delivery(request, orderID):
    to_email = []
    order = Order.objects.get(id=orderID)
    order.confirmDelivery()
    order.save()
    mail_subject = 'Order Delivered successfully'
    to = str(order.customer.customer.email)
    to_email.append(to)
    from_email = 'abhinavparakh19@gmail.com'
    message = "Hi "+order.customer.customer.first_name+" Your order was delivered successfully. Please go to your dashboard to see your order history. <br> Your order id is "+orderID+". Share ypour feedback woth us."
    send_mail(
        mail_subject,
        message,
        from_email,
        to_email,
    )
    return redirect('orders_admin')
#CART FUNCTIONALITY
@login_required
def addTocart(request, foodID, userID):
    food = Dish.objects.get(id=foodID)
    user = User.objects.get(id=userID)
    tart = Cart.objects.filter(dish=food,user=user)
    if tart.exists():
        cart = Cart.objects.get(dish=food,user=user)
        cart.quantity= cart.quantity + 1
        cart.save() 
    else:
        cart = Cart.objects.create(dish=food, user=user)
        cart.save()
    return redirect('cart')

@login_required
def delete_item(request, ID):
    item = Cart.objects.get(id=ID)
    item.delete()
    return redirect('cart')


@login_required
def cart(request):
    user = User.objects.get(id=request.user.id)
    items = Cart.objects.filter(user=user)
    total = 0
    for item in items:
        total += item.dish.sale_price * item.quantity
    return render(request, 'cart.html', {'items': items, 'total':total})

#PLACE ORDER
@login_required
def placeOrder(request):
    to_email = []
    customer = Customer.objects.get(customer=request.user)
    print(customer.address)
    items = Cart.objects.filter(user=request.user)
    total_amt=0
    for item in items:
        food = item.dish
        total_amt += food.sale_price *item.quantity
    order = Order.objects.create(customer=customer, order_timestamp=timezone.now(), payment_status="Pending", 
    delivery_status="Pending", total_amount=total_amt, payment_method="Cash On Delivery", location=customer.address)
    order.save()
    for item in items:
        food=item.dish
        orderContent = OrderContent(dish=food, order=order)
        orderContent.save()
        item.delete()
    mail_subject = 'Order Placed successfully'
    to = str(customer.customer.email)
    to_email.append(to)
    from_email = 'abhinavparakh19@gmail.com'
    message = "Hi "+customer.customer.first_name+" Your order was placed successfully. Please go to your dashboard to see your order history. <br> Your order id is "#+order.id+""
    send_mail(
        mail_subject,
        message,
        from_email,
        to_email,
    )
    return redirect('cart')



@login_required
def cust_profile(request):
    cust =  Customer.objects.filter(customer = request.user )
    cons =  cust[0]
    print(cust[0].address)
    return render(request,'customer_temp/project3.html',{'users':cons})

@login_required
def user_profile(request):
    cust =  Customer.objects.filter(customer = request.user )
    cons =  cust[0]
    print(cust[0].address)
    return render(request,'customer_temp/project3.html',{'users':cons})


@login_required
def my_orders(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(customer=user)
    orders = Order.objects.filter(customer=customer)
    return render(request, 'customer_temp/orders.html', {'orders': orders})


def user_behaviour(request,food):
    #getting customer ids
    user = Customer.objects.all()
    cust_ids=[]
    custs=[]
    for cust in user:
        cust_ids.append(cust.id)
    #getting orderids corresponding to customer ids
    ord={}
    for c in cust_ids:
        ord[c]=[]
        orde = Order.objects.filter(customer__id=c)
        for o in orde:
            ord[c].append(o.id)
    #keeping track of most ordered dish 
    beh={}
    for c in cust_ids:
        beh[c]={}
    for c in cust_ids:
        for k in ord[c]:
            oc = OrderContent.objects.filter(order__id=k)
            for o in oc:
                beh[c][o.dish]=0
    for c in cust_ids:
        for k in ord[c]:
            oc = OrderContent.objects.filter(order__id=k)
            for o in oc:
                beh[c][o.dish]+=o.quantity
    #building track of behaviour
    for c in cust_ids:
        if beh[c]!={}:
            max_val=max(beh[c].values())
            if beh[c][food] == max_val :
                print("sendmail",Customer.objects.get(id=c))
                custs.append(User.objects.get(customer__id=c))
                print(custs)
    return custs