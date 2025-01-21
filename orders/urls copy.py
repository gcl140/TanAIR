from django.urls import path
from . import views

urlpatterns = [
    # Logistics Worker Views
    path('logistics-dashboard/', views.logistics_dashboard, name='logistics_dashboard'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('create-item/', views.create_item, name='create_item'),

    # User Views
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
]
