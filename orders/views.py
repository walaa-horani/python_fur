from tkinter.messagebox import NO
from unicodedata import category
from django.shortcuts import get_object_or_404, render, redirect
from  django.contrib import messages
from  store.models import  Product
from  orders.models import Order,OrderDetails
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Payment
from store.models import Category

from  django.utils import  timezone
# Create your views here.
@login_required 
def add_to_cart(request):
    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.GET['pro_id']
        qty = request.GET['qty']

        order = Order.objects.filter(user=request.user, is_finished=False)
        if not Product.objects.filter(id=pro_id).exists():
            return redirect('product')
        pro = Product.objects.get(id=pro_id)
        if order:
            messages.success(request, 'your product has been added to cart')

            old_order = Order.objects.get(user=request.user, is_finished=False)

            if OrderDetails.objects.filter(order=old_order, product=pro).exists():
                orderdetails = OrderDetails.objects.get(order=old_order, product=pro)
                orderdetails.quantity += int(qty)
                orderdetails.save()
            else:
                orderdetails = OrderDetails.objects.create(product=pro, order=old_order, price=pro.price,
                                                                 quantity=qty)

        else:
            messages.success(request, 'your product has been added to cart')
            new_order = Order()
            new_order.user = request.user
            new_order.is_finished = False
            new_order.save()
            orderdetails = OrderDetails.objects.create(product=pro, order=new_order, price=pro.price,
                                                             quantity=qty)
    else:
        messages.error(request,'please log in to add it to cart')
        

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))




def cart(request):
    category =Category.objects.all()
    context= None
    if request.user.is_authenticated and not request.user.is_anonymous:

        if Order.objects.filter(user=request.user, is_finished=False):
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails= OrderDetails.objects.filter(order=order)

            total = 0
            for sub in orderdetails:
                total += sub.price * sub.quantity

            
            context = {
                'order':order,
                'orderdetails': orderdetails,
                'total': total,
                'category':category
            }
    return render(request,'order/cart.html', context)

def remove_from_cart(request, orderdetails_id):
        if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
            orderdetails = OrderDetails.objects.get(id=orderdetails_id)
            if orderdetails.order.user.id == request.user.id:
                orderdetails.delete()
        return redirect('cart')

def remove_fav(request, orderdetails_id):
        if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
           product= get_object_or_404(Product,pk=orderdetails_id)
           
           
           product.delete()
                
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def add_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        orderdetails.quantity += 1
        orderdetails.save()
    return redirect('cart')


def sub_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.quantity > 1:
            orderdetails.quantity -= 1
        orderdetails.save()
    return redirect('cart')




def show_orders(request):
    category = Category.objects.all()
    context = None
    all_orders = None
    if request.user.is_authenticated and not request.user.is_anonymous:

            all_orders = Order.objects.filter(user=request.user )
            if all_orders:
                for x in all_orders:
                    order = Order.objects.get(id=x.id)
                    orderdetails= OrderDetails.objects.filter(order=order)

                    total = 0
                    for sub in orderdetails:
                        total += sub.price * sub.quantity
                    x.total  = total 
                    x.items_count = orderdetails.count

    context = {'all_orders':all_orders,'category':category}            
    return render(request,'order/show_orders.html', context)



def checkout(request):
    
   
    context = None
    ship_address = None
    ship_phone = None
    expire = None
    card_number = None
    security_code = None
    is_added = None
    if request.method == 'POST' and 'payment' in request.POST and 'ship_address' in request.POST and 'ship_phone' in request.POST and 'expire' in request.POST and 'card_number' in request.POST and 'security_code' in request.POST:
                ship_address = request.POST['ship_address']
                ship_phone = request.POST['ship_phone']
                expire = request.POST['expire']
                card_number = request.POST['card_number']
                security_code = request.POST['security_code']

                if request.user.is_authenticated and not request.user.is_anonymous:

                  if Order.objects.filter(user=request.user, is_finished=False):
                     order = Order.objects.get(user=request.user, is_finished=False)
                     payment = Payment(order = order, shipment_address=ship_address,shipment_phone=ship_phone,card_number=card_number,expire=expire,security_code=security_code)
                     payment.save()
                     order.is_finished = True
                     order.save()
                     is_added = True
                     messages.success(request,'your order is finished')


         
         
        
        
        

                context = {
                        'ship_address':ship_address,
                        'ship_phone':ship_phone,
                        'card_number':card_number,
                        'expire':expire,
                        'security_code':security_code,
                        'is_added':is_added
        }
    else:
            
        if request.user.is_authenticated and not request.user.is_anonymous:

            if Order.objects.filter(user=request.user, is_finished=False):
                order = Order.objects.get(user=request.user, is_finished=False)
                orderdetails= OrderDetails.objects.filter(order=order)

                total = 0
                for sub in orderdetails:
                    total += sub.price * sub.quantity


                context = {
                    'order':order,
                    'orderdetails': orderdetails,
                    'total': total,
                    
                }

    return render(request,'order/checkout.html', context)
