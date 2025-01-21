from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Order, Item
from .forms import OrderForm, ItemForm  # Include ItemForm if you're creating items.
import uuid  # Add this at the top for UUID generation

# Custom decorator to ensure only logistics workers can access
def logistics_worker_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'logisticsworker'):
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper

# Logistics Dashboard - Where logistics workers can manage orders
@logistics_worker_required
def logistics_dashboard(request):
    items = Item.objects.all()
    orders = Order.objects.all()
    return render(request, 'orders/logistics_dashboard.html', {'items': items, 'orders': orders})



# Place order with a unique order ID
@login_required
def place_order(request):
    item_id = request.GET.get('item_id')
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        
        if item.stock < quantity:
            messages.error(request, "Not enough stock available.")
        else:
            # Generate a unique order ID using UUID
            unique_order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"  # Shortened UUID for readability
            
            order = Order.objects.create(
                order_id=unique_order_id,  # Use the unique order ID
                customer_name=request.user.first_name,
                product_name=item.name,
                quantity=quantity,
                price=item.price,
                total_price=item.price * quantity,
                status='Pending'
            )
            # Update the stock
            item.stock -= quantity
            item.save()
            messages.success(request, f"Order placed successfully! Your Order ID is {unique_order_id}.")
            return redirect('user_dashboard')

    return render(request, 'orders/place_order.html', {'item': item})

# Update order status and display user and ID in messages
@logistics_worker_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Get order or 404 error
    if request.method == 'POST':
        new_status = request.POST.get('status')  # Get new status from form
        order.status = new_status
        order.save()
        
        # Use the order's ID and customer name in the message
        messages.success(
            request,
            f"{order.customer_name}'s order with ID #{order.order_id} has been updated to '{new_status}'."
        )
        return redirect('logistics_dashboard')  # Redirect back to logistics dashboard
    return render(request, 'orders/update_order_status.html', {'order': order})

# Order confirmation page
@login_required
def order_confirmation(request):
    return render(request, 'orders/order_confirmation.html')

# User Dashboard - View all orders placed by the user
@login_required
def user_dashboard(request):
    items = Item.objects.all()  # Fetch all items to display to the user
    orders = Order.objects.filter(customer_name=request.user.first_name)
    return render(request, 'orders/user_dashboard.html', {'items': items, 'orders': orders})

# Create an item view - For creating new items (admin/logistics workers)
@logistics_worker_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Item created successfully!")
            return redirect('logistics_dashboard')  # Redirect to logistics dashboard
    else:
        form = ItemForm()
    return render(request, 'orders/create_item.html', {'form': form})

# Delete an order - for logistics workers
# @logistics_worker_required
@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    # messages.success(request, f"Order #{order.id} has been deleted.")
    messages.success(
            request,
            f"{order.customer_name}'s order with ID #{order.order_id} has been deleted."
        )
    if hasattr(request.user, 'logisticsworker'):
        return redirect('logistics_dashboard')
    else: return redirect('user_dashboard')


@logistics_worker_required
def delete_item(request, name):
    item = get_object_or_404(Item, name=name)
    item.delete()
    messages.success(request, f"Item {name} has been deleted.")
    return redirect('logistics_dashboard')





@logistics_worker_required
def update_item(request, item_name):
    item = get_object_or_404(Item, name=item_name)
    if request.method == 'POST':
        form = ItemUpdateForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item '{item.name}' has been updated successfully.")
            return redirect('logistics_dashboard')
    else:
        form = ItemUpdateForm(instance=item)
    
    return render(request, 'yuzzaz/update_item.html', {'form': form, 'item': item})
