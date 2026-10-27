from django.db import models
import uuid
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self): 
        return self.name

class Supplier(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    address=models.TextField()

    def __str__(self): 
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    barcode=models.CharField(max_length=50,unique=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()

    def __str__(self): 
        return self.name


class Bill(models.Model):
    customer_name=models.CharField(max_length=100,blank=True)
    payment_method=models.CharField(max_length=20,default="Cash")
    phone=models.CharField(max_length=15,blank=True)
    bill_date=models.DateTimeField(auto_now_add=True)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    receipt_token=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)

    def __str__(self):
        return f"Bill {self.id}"

class Billitem(models.Model):
    bill=models.ForeignKey(Bill,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    total=models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __str__(self):
        return self.product.name


# Create your models here.