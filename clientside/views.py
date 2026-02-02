from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
from .models import *
from adminside.models import *

def index(request):
    return render(request, 'index.html')
    
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['is_logged_in'] = True
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    auth_logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        email = request.POST.get('email')
        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                messages.success(request, "Registration successful")
                return redirect('login')
        else:
            messages.error(request, "Password not matched")
    return render(request, 'register.html')

def feedback(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        rating = request.POST.get('rating')
        message = request.POST.get('message')
        Feedback.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            rating=rating,
            message=message
        )
        messages.success(request, "Feddback Send Successfully!")
        return redirect('feedback')
    return render(request, 'feedback.html')


def contact(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            subject=subject,
            message=message
        )
        messages.success(request, "Contact Send Successfully!")
        return redirect('contact')
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def viewproduct(request, category, type):

    products = Product.objects.filter(category=category, type=type)

    return render(request, 'viewproduct.html', {
        'product': products,
        'category': category,
        'type': type,
    })

def add_to_cart(request, pid):
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        cart[str(pid)] = cart.get(str(pid), 0) + 1
        request.session['cart'] = cart
        request.session.modified = True
    else:
        product = Product.objects.get(id=pid)
        item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            item.qty += 1
            item.save()
    return redirect('cart')


def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        return render(request, 'cart.html', {'cart_items': cart_items})
    else:
        cart = request.session.get('cart', {})
        return render(request, 'cart.html', {'cart': cart})

def delete_cart(request, id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(
            CartItem,
            user=request.user,
            product_id=id
        )
        cart_item.delete()
    else:
        cart = request.session.get('cart', {})
        id = str(id)

        if id in cart:
            del cart[id]

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')

def order_form(request, pid):
    product = get_object_or_404(Product, id=pid)
    qty = request.GET.get('qty', 1) 

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size', 'M')
        total_price = product.price * quantity
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        Order.objects.create(
            product=product,
            product_name=product.name,
            size=size, 
            quantity=quantity,
            price=product.price,
            total_price=total_price,
            mobile=mobile,
            address=address,
            user=request.user if request.user.is_authenticated else None
        )

        return redirect('vieworder')

    return render(request, 'orderform.html', {'product': product, 'quantity': qty})



def vieworder(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = []

    return render(request, 'vieworder.html', {'orders': orders})

def delete_order(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    order.delete()
    return redirect('vieworder')