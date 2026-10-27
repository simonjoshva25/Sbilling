from django.contrib import admin
from billing.models import Category,Supplier,Product,Bill,Billitem
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name']
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display=['id','name','phone','address']
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','category','supplier','price','stock']
    search_fields=['name','barcode']
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display=['id','bill_date','customer_name','total_amount']
@admin.register(Billitem)
class BillitemAdmin(admin.ModelAdmin):
    list_display=['id','bill','product','quantity','price']

# Register your models here.
