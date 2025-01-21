from django.urls import path
from yuzzaz import views as yuzzaz_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('logistics-dashboard/', views.logistics_dashboard, name='logistics_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('place-order/', views.place_order, name='place_order'),
    path('create-item/', views.create_item, name='create_item'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),  # Ensure this line exists
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),  # Ensure this line exists
    path('delete_item/<str:name>/', views.delete_item, name='delete_item'),
    path('update_item/<str:item_name>/', views.update_item, name='update_item'),
    path('logout/', yuzzaz_views.logout, name='logout')
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
