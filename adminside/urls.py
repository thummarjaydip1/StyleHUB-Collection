from django.contrib import admin
from django.urls import path
from adminside import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_index/',views.admin_index,name="admin_index"),
    path('admin_logout/',views.admin_logout,name="admin_logout"),
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('admin_contact/',views.admin_contact,name="admin_contact"),
    path('admin_contact_delete/<int:id>/',views.admin_contact_delete,name="admin_contact_delete"),
    path('admin_feedback/',views.admin_feedback,name="admin_feedback"),
    path('admin_feedback_delete/<int:id>/',views.admin_feedback_delete,name="admin_feedback_delete"),
    path('admin_add_product/',views.admin_add_product,name="admin_add_product"),
    path('admin_view_product/',views.admin_view_product,name="admin_view_product"),
    path('admin_update_product/<int:id>',views.admin_update_product,name="admin_update_product"),
    path('admin_delete_product/<int:id>',views.admin_delete_product,name="admin_delete_product"),
    path('admin_orders/',views.admin_orders,name="admin_orders"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)