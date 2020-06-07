from django.shortcuts import render, redirect

from .models import Product, Order, OrderItem, Customer, ShippingAddress

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import CustomerForm,CheckoutForm
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json
# Create your views here.

def sign_in(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        customer= authenticate(request, username=username, password=password)

        if customer is not None:
            login(request, customer)
            return redirect("home_page")
        else:
            return redirect("sign_in")
    return render(request,"customer/sign_in.html",{})

def signOut(request):
    logout(request)
    return redirect("home_page")

def home_page(request):
    products = Product.objects.all()
    paginator = Paginator(products,8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        "items": items,
        "page":"home",
        "items_page": items,
        "page_range": page_range,
    }
    return render(request,'customer/home_page.html',context)

def shirts_page(request):
    products = Product.objects.filter(category="s")
    paginator = Paginator(products,8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        "items": items,
        "page":"shirts",
        "items_page": items,
        "page_range": page_range,
    }
    return render(request,'customer/home_page.html',context)

def sports_wear_page(request):
    products = Product.objects.filter(category="SW")
    paginator = Paginator(products,8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        "items": items,
        "page":"sports-wear",
        "items_page": items,
        "page_range": page_range,
    }
    return render(request,'customer/home_page.html',context)

def outwear_page(request):
    products = Product.objects.filter(category="OW")
    paginator = Paginator(products,8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        "items": items,
        "page":"outwear",
        "items_page": items,
        "page_range": page_range,
    }
    return render(request,'customer/home_page.html',context)

@login_required(login_url="sign_in")
def cart(request):
    customer = request.user.customer
    try:
        order  = Order.objects.get(customer=customer, complete=False)
        items = order.orderitem_set.all()
    except ObjectDoesNotExist:
        order = []
        items = []

    return render(request,"customer/cart.html",{"items":items,"order":order})

@login_required(login_url="sign_in")
def checkout(request):
    customer = request.user.customer
    try:
        order = Order.objects.get(customer=customer, complete=False)
        items = order.orderitem_set.all()
    except ObjectDoesNotExist:
        
        return redirect("home_page")
    total_items = 0
    for i in items:
        q = i.quantity
        total_items += q
    form = CheckoutForm()
    try:
        order = Order.objects.get(customer=request.user.customer, complete=False)
        if request.method=="POST":
            form = CheckoutForm(request.POST)
            if form.is_valid():
                street  = form.cleaned_data.get("street")
                apartment = form.cleaned_data.get("apartment")
                city = form.cleaned_data.get("city")
                zip_code = form.cleaned_data.get("zip_code")
                # payment_info = form.cleaned_data.get("payment_info")

                ShippingAddress.objects.create(
                    customer = request.user.customer,
                    order = order,
                    street = street,
                    city = city,
                    apartment = apartment,
                    zipcode = zip_code
                )
                order.complete = True
                order.save()
                messages.success(request,'Your order has been received')
                return redirect('home_page')
            else:
                messages.success(request,'Checkout failed')
                return redirect('home_page')

    except ObjectDoesNotExist:
        messages.success(request,'Checkout failed')
        return redirect("checkout")
    context = {
        "items":items,
        "order":order,
        'item_count':items.count,
        "form":form
    }
    return render(request,"customer/checkout.html",context)

def product_detail(request,id):
    product = Product.objects.get(id=id)

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        customer= authenticate(request, username=username, password=password)

        if customer is not None:
            login(request, customer)
            return redirect("product_detail", id=id)
        else:
            return redirect("product_detail", id=id)
    context = {
        "item":product
    }
    return render(request,"customer/product_detail.html",context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order , created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("item was added", safe=False)


def register(request):
    form = CustomerForm()
    if request.method=="POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")

            Customer.objects.create(
                customer = customer,
                name = name,
                email = email
            )
            messages.info(request,'Your account has been created')
            return redirect("sign_in")
            
    context={
        "form":form
    }
    return render(request,"customer/register.html",context)