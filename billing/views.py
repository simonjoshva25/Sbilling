from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from django.db import transaction
from billing.models import Product,Bill,Billitem
from billing.forms import ProductForm
def product_list(request):
    query=request.GET.get('search')
    if query:
        if query.isdigit():
            products=Product.objects.filter(
                Q(id=query)|
                Q(barcode__icontains=query)
                )
        else:
            products=Product.objects.filter(
                Q(name__icontains=query)|
                Q(barcode__icontains=query)
            )
    else:
        products=Product.objects.all()
    return render(request,'product.html',{'s':products})
def add_product(request):
    form=ProductForm()
    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/product')

    return render(request,'add_product.html',{'form':form})

def update(request,id):
    u=get_object_or_404(Product,id=id)
    if request.method=="POST":
        form=ProductForm(request.POST,instance=u)
        if form.is_valid():
            form.save()
            return redirect('/product')
    else:
        form=ProductForm(instance=u)
    return render(request,'update.html',{'form':form})
def delete(request,id):
    p=Product.objects.get(id=id)
    p.delete()
    return redirect('/product')

def billing(request):
    products=Product.objects.all()
    bill_items=request.session.get("bill_items",[])
    grand_total=0
    search=request.GET.get('search')
    if search:
        products=Product.objects.filter(name__icontains=search)
    if request.method=="POST":
        product_id=request.POST.get("product_id")
        quantity=int(request.POST.get("quantity",1))
        product=Product.objects.get(id=product_id)
        if quantity>product.stock:
            grand_total=sum(item["total"]for item in bill_items)
            return render(request,'billing.html',{'products':products,'bill_items':bill_items,'grand_total':bill_items,'grand_total':sum(item['total']for item in bill_items),'error':'insuficient stock'})
        found=False
        for item in bill_items:
            if item['id']==product.id:
                item['quantity']+=quantity
                item['total']=item['quantity']*float(product.price)
                found=True
                break
        if not found:
            total=quantity*float(product.price)
            bill_items.append({"id":product.id,"name":product.name,"price":float(product.price),"quantity":quantity,"total":float(total)})

        request.session['bill_items']=bill_items
        request.session.modified=True
    grand_total=sum(item['total'] for item in bill_items)
    context={
        "products":products,
        "bill_items":bill_items,
        "grand_total":grand_total,
        }
    return render(request,"billing.html",context)
def remove(request,product_id):
    bill_items=request.session.get("bill_items",[])
    bill_items=[item for item in bill_items if item["id"]!=product_id]
    request.session['bill_items']=bill_items
    request.session.modified=True
    return redirect("billing")
def clear(request):
    request.session["bill_items"]=[]
    request.session.modified=True
    return redirect("billing")
def checkout(request):
    bill_items=request.session.get('bill_items',[])
    if not bill_items:
        return redirect("billing")
    grand_total=sum(float(item["total"])for item in bill_items)
    if request.method=="POST":
        customer_name=request.POST.get("customer_name","Walk-in Customer")
        payment_method=request.POST.get("payment_method","Cash")
        customer_no=request.POST.get('mobile_no')
        with transaction.atomic():
            bill=Bill.objects.create(customer_name=customer_name,phone=customer_no,payment_method=payment_method,total_amount=grand_total)
        for item in bill_items:
            product=Product.objects.get(id=item["id"])
            quantity=int(item["quantity"])
            if quantity>product.stock:
                return render(request,"billing.html",{"products":
                Product.objects.all(),
                "bill_items":bill_items,
                "grand_total":grand_total,
                "error": f"Not enough stock for{product.name}"
                }
            )
            Billitem.objects.create(bill=bill,product=product,quantity=quantity,price=product.price,total=product.price*quantity)
            product.stock-=quantity
            product.save()
        request.session['bill_items']=[]
        request.session.modified=True
        return render(request,'bill_success.html',{'bill':bill,'bill_items':bill_items})
    return render(request,'checkout.html',{"bill_items":bill_items,"grand_total":grand_total})

