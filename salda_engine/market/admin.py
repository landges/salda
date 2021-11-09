from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'article', 'category', 'alter_category','price')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id','name','slug','service')


@admin.register(ProductInBasket)
class ProductInBasketAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'order', 'product', 'nmb', 'price_per_item', 'total_price', 'is_active')
    list_filter = ('session_key', 'is_active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status')
    list_filter = ('payment', 'delivery')
    # inlines = [ProductInOrderInline]
    search_fields = ('user',)
    list_display_links = ("user",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')


@admin.register(ProductInOrder)
class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = ('id','order','product')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'point', 'address')

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')