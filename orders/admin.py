from django.contrib import admin
from .models import Order, LogisticsWorker, Item

# Customizing the admin interface for the Order model
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'product_name', 'quantity', 'price', 'status', 'created_at')
    search_fields = ('order_id', 'customer_name', 'product_name')
    list_filter = ('status',)
    ordering = ('-created_at',)  # Order by most recent

    # Make the status field editable in the list view
    list_editable = ('status',)

# Customizing the admin interface for the Item model
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'image')
    search_fields = ('name',)
    list_filter = ('price',)
    ordering = ('-id',)  # Order by most recent

# Register models with the custom admin interfaces
admin.site.register(Item, ItemAdmin)  # Register Item once
admin.site.register(Order, OrderAdmin)  # Register Order with custom admin
admin.site.register(LogisticsWorker)  # Register LogisticsWorker
