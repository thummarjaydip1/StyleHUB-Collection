from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from clientside.models import *
from django.contrib import messages

def admin_dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('admin_index')
    else:
        context = {
        'total_users': User.objects.count(),
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
    }
    return render(request, "admin_dashboard.html",context)

def admin_contact(request):
    if not request.session.get('admin_id'):
        return redirect('admin_index')
    
    data = Contact.objects.all()
    return render(request, "admin_contact.html", {'data': data})


def admin_contact_delete(request, id):
    if not request.session.get('admin_id'):
        return redirect('admin_index')
    
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    return redirect('admin_contact')

def admin_feedback(request):
    if not request.session.get('admin_id'):
        return redirect("admin_index")
    
    data = Feedback.objects.all()
    return render(request, "admin_feedback.html", {'data': data})


def admin_feedback_delete(request, id):
    if not request.session.get('admin_id'):
        return redirect('admin_index')
    
    feedback = get_object_or_404(Feedback, id=id)
    feedback.delete()
    return redirect('admin_feedback')

def admin_index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        admin = Adminlogin.objects.filter(
            username=username,
            password=password
        ).first()
        if admin:
            request.session['admin_id'] = admin.id
            request.session['admin_username'] = admin.username
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_index.html', {
                'error': 'Invalid Username or Password'
            })
    return render(request, 'admin_index.html')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_index')

def admin_add_product(request):
    if not request.session.get('admin_id'):
        return redirect("admin_index")
    
    if request.method == "POST":
        name = request.POST.get('name')
        category = request.POST.get('category')
        type_ = request.POST.get('type')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        Product.objects.create(
            name=name,
            category=category,
            type=type_,
            price=price,
            image=image
        )
        messages.success(request, "Product added successfully")
        return redirect('admin_view_product')
    return render(request, "admin_add_product.html")

def admin_view_product(request):
    if not request.session.get('admin_id'):
        return redirect("admin_index")
    else:
        data=Product.objects.all()
    return render(request, "admin_view_product.html", {'data': data})

def admin_update_product(request, id):
    if not request.session.get('admin_id'):
        return redirect("admin_index")
    else:
        product = Product.objects.get(id=id)
        if request.method == "POST":
            product.name = request.POST['name']
            product.category = request.POST['category']
            product.type = request.POST['type']
            product.price = request.POST['price']

            if 'image' in request.FILES:
                product.image = request.FILES['image']

            product.save()
            return redirect('admin_view_product')

        return render(request, 'admin_update_product.html', {'product': product})

def admin_delete_product(request, id):
    if not request.session.get('admin_id'):
        return redirect("admin_index")
    
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('admin_view_product')

def admin_orders(request):
    if not request.session.get('admin_id'):
        return redirect("admin_index")
    else:
        orders = Order.objects.all().order_by('-id') 
        return render(request, 'admin_view_order.html', {'orders': orders})

