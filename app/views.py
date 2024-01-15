from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if the product is already in the cart
        cart_items, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_items.quantity += 1
        cart_items.save()

        return redirect('view_cart')
    else:
        # Handle the case where the user is not authenticated
        return redirect('index')

@login_required
def view_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        cart_items = cart.get_cart_items
        count_items = cart.get_total_items
        total_price = cart.get_cart_total
        user_notlogin = "hidden"
        user_login = "show"
    else:
        items = []
        cart = {'get_cart_items': 0, 'get_cart_total': 0}
        cart_items = cart['get_cart_items']
        count_items = 0
        user_notlogin = "hidden"
        user_login = "show"

    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', "")
    products = Product.objects.all()

    context = {
        'cart_items': cart_items, 
        'items': items, 
        'cart': cart, 
        'active_category': active_category, 
        'categories': categories, 
        'products': products, 
        "count_items": count_items,
        'total_price': total_price, 
        'user_notlogin': user_notlogin, 
        'user_login': user_login
    }
    return render(request, 'app/cart.html', context)


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        cart_items = cart.get_cart_items
        count_items = cart.get_total_items
        user_notlogin = "hidden"
        user_login = "show"
    else:
        items = []
        cart = {'get_cart_items': 0, 'get_cart_total': 0}
        cart_items = cart['get_cart_items']
        count_items = 0
        user_notlogin = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', "")
    products = Product.objects.all()
    context = {
        'active_category': active_category, 
        'categories': categories, 
        'products': products,
        'cart_items': cart_items, 
        "user_login": user_login, 
        "user_notlogin": user_notlogin, 
        "count_items": count_items
    }
    return render(request, 'app/home.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'user or password not correct!')
    context = {}
    return render(request, 'app/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'app/register.html', context)

def search(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        keys = Product.objects.filter(name__contains=searched)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        cart_items = cart.get_cart_items
    else:
        items = []
        cart = {'get_cart_items': 0, 'get_cart_total': 0}
        cart_items = cart['get_cart_items']
    products = Product.objects.all()

    return render(request, 'app/search.html', {"searched": searched, "keys": keys, "cart_items": cart_items, "products": products})

def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', "")
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    context = {
        "categories": categories,
        "active_category": active_category, 
        "products": products
    }
    return render(request, 'app/category.html', context)

def detail(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        cart_items = cart.get_cart_items
        count_items = cart.get_total_items
        user_notlogin = "hidden"
        user_login = "show"
    else:
        items = []
        cart = {'get_cart_items': 0, 'get_cart_total': 0}
        cart_items = cart['get_cart_items']
        count_items = 0
        user_notlogin = "show"
        user_login = "hidden"
    id = request.GET.get('id', '')
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', "")
    products = Product.objects.filter(id=id)
    context = {
        "products": products, 
        'active_category': active_category, 
        'categories': categories,
        'products': products, 
        'cart_items': cart_items, 
        "user_login": user_login, 
        "user_notlogin": user_notlogin,
        'count_items': count_items
    }
    return render(request, 'app/detail.html', context)
