from django.contrib import admin
from django.urls import path
from clientside import views

urlpatterns = [
    path('index/',views.index,name="index"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('register/',views.register,name="register"),
    path('feedback/',views.feedback,name="feedback"),
    path('contact/',views.contact,name="contact"),
    path('about/',views.about,name="about"),
    path('viewproduct/<str:category>/<str:type>',views.viewproduct,name="viewproduct"),
    path('add-to-cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('delete_cart/<int:id>/', views.delete_cart, name='delete_cart'),
    path('order/<int:pid>/', views.order_form, name='order_form'),
    path('vieworder/', views.vieworder, name='vieworder'),
    path('delete_order/<int:id>/', views.delete_order, name='delete_order')
]
