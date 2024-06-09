from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,DetailView
from django.views import View
from account.models import product,cart,orders
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail

# decorator
def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.info(request,"please login first!!")
            return redirect('log')
    return inner

decorators=[signin_required,never_cache]

# Create your views here.
@method_decorator(decorators,name='dispatch')
class HomeView(TemplateView):
    template_name="home.html"


# der(request,"products.html")
@method_decorator(decorators,name='dispatch')
class ProductsView(ListView):
    template_name="products.html"
    queryset=product.objects.all()
    context_object_name="data"

    def get_queryset(self) -> QuerySet[Any]:
        qs=super().get_queryset()
        qs=qs.filter(category=self.kwargs.get('cat'))
        return qs
    
@method_decorator(decorators,name='dispatch')    
class ProductsDetailsView(DetailView):
    template_name="details.html"
    queryset=product.objects.all()
    pk_url_kwarg="pid"
    context_object_name="product"

decorators
def addtoCart(request,*args,**kwargs):
    try:
        user=request.user
        pid=kwargs.get('pid')
        Product=product.objects.get(id=pid)
        try:
            Cart=cart.objects.get(user=user,product=Product)
            Cart.quantity+=1
            Cart.save()
            messages.success(request,"product quantity updated!!")
            return redirect('chome')
        except:
            cart.objects.create(user=user,product=Product)
            messages.success(request,"product added to cart!!")
            return redirect('chome')

    except:
        messages.error(request,"cart entry failed!!")
        return redirect('chome')
    

@method_decorator(decorators,name='dispatch')    
class CartListView(ListView):
    template_name="cartlist.html"
    queryset=cart.objects.all()
    context_object_name="cart"

    def get_queryset(self) -> QuerySet[Any]:
        qs=super().get_queryset()
        print(qs)
        qs=qs.filter(user=self.request.user)
        return qs
    
decorators    
def DeleteCart(request,*args,**kwargs):
    try:
        cid=kwargs.get('id')
        Cart=cart.objects.get(id=cid)
        
        Cart.quantity-=1
        Cart.delete()
        messages.success(request,"product deleted!!")
        return redirect('clist')
        
    except:
        messages.error(request,"cart deletion failed!!")
        return redirect('clist')
    

@method_decorator(decorators,name='dispatch')    
class CheckoutView(TemplateView):
    template_name="checkout.html"

    def post(self,request,*args,**kwargs):
        try:
            cid=kwargs.get('cid')
            Cart=cart.objects.get(id=cid)
            product=Cart.product
            user=Cart.user
            ph=request.POST.get('phone')
            add=request.POST.get('address')
            orders.objects.create(product=product,user=user,phone=ph,address=add)
            Cart.delete()
            messages.success(request,"order placed successfullu!!")
            return redirect('clist')
        except Exception as e:
            print(e)
            messages.error("order failed")
            return redirect('clist')
        
            
@method_decorator(decorators,name='dispatch')
class OrderListView(ListView):
    template_name="orders.html"
    queryset=orders.objects.all()
    context_object_name="order"

    def get_queryset(self):
        qs=super().get_queryset()
        qs=qs.filter(user=self.request.user)
        return qs

decorators    
def cancelOrder(request,*args,**kwargs):
    try:
        oid=kwargs.get('oid')
        order=orders.objects.get(id=oid)
        subject="order cancelling aknowledgment"
        msg=f"your order for {order.product.title} is successfully cancelled!!"
        fr_om="hasnathkp.006@gmail.com"
        to_ad=[request.user.email]
        send_mail(subject,msg,fr_om,to_ad)
        order.delete()
        messages.success(request,"order cancelled!!")
        return redirect('olist')
    except Exception as e:
        messages.error(request.e)
        return redirect('olist')