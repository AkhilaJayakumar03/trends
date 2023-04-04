from django.urls import path
from.views import *


urlpatterns=[
    path('index/',index),
    path('shopregister/',shopregister),
    path('shoplogin/',shoplogin),
    path('shopprofile/',shopprofile),
    path('productupload/',productupload),
    path('productdisplay/',productdisplay),
    path('delete/<int:id>',productdelete),
    path('edit/<int:id>',productedit),
    path('home/',home),
    path('userregister/',userregister),
    # path('success/',success),
    path('verify/<auth_token>',verify),
    path('userlogin/',userlogin),
    path('userprofile/',userprofile),
    path('men/',mendisplay),
    path('women/',womendisplay),
    path('menbag/',menbag),
    path('menclothing/',menclothing),
    path('menwatch/',menwatch),
    path('menshoe/',menshoe),
    path('womenbag/',womenbag),
    path('womenclothing/',womenclothing),
    path('womenwatch/',womenwatch),
    path('womenshoe/',womenshoe),
    path('viewallproducts/',viewallproducts),
    path('viewproducts/',viewproducts),
    path('addtocart/<int:id>',addtocart),
    path('cartdisplay/',cartdisplay),
    path('cartitemremove/<int:id>',cartitemremove),
    path('addtowishlist/<int:id>',addtowishlist),
    path('wishlistdisplay/',wishlistdisplay),
    path('wishitemremove/<int:id>',wishitemremove),
    path('wishtocart/<int:id>',wishtocart),
    path('buyproduct/<int:id>',buyproduct),
    path('payment/',payment),
    path('usernotification/',usernotification),
    path('shopnotification/',shopnotification),
    path('logout/',user_logout),
path('shoplogout/',shop_logout)
]