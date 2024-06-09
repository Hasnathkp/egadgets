from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[
             path('chome',HomeView.as_view(),name="chome"),
             path('prod<str:cat>',ProductsView.as_view(),name="prod"),
             path('pdet<int:pid>',ProductsDetailsView.as_view(),name="pdet"),
             path('addcart/<int:pid>',addtoCart,name="acart"),
             path('cartlist',CartListView.as_view(),name="clist"),
             path('dcart<int:id>',DeleteCart,name="dcart"),
             path('checkout/<int:cid>',CheckoutView.as_view(),name="ckout"),
             path('orderlist',OrderListView.as_view(),name="olist"),
             path('cancelorder/<int:oid>',cancelOrder,name="cancel")
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)