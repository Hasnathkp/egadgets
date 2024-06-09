from account.models import cart,orders

def cart_count(request):
    if request.user.is_authenticated:
       count=cart.objects.filter(user=request.user).count()
       return{"count":count}
    else:
        return{"count":0}

def order_count(request):
    if request.user.is_authenticated:
        count=orders.objects.filter(user=request.user).count()
        return{"orderr":count}
    else:
        return{"orderr":0}
