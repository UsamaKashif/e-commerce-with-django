from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("",views.home_page,name="home_page"),
    path("shirts",views.shirts_page,name="Shirt"),
    path("sports-wear",views.sports_wear_page,name="Sport Wear"),
    path("outwear",views.outwear_page,name="Outwear"),
    
    path("checkout/",views.checkout,name="checkout"),
    path("product-detail/<int:id>/",views.product_detail,name="product_detail"),
    path("cart/",views.cart,name="cart"),
    path("update_item/",views.update_item,name="update_item"),
    path("sign-in/",views.sign_in,name="sign_in"),
    path("sign-out/",views.signOut,name="sign_out"),
    path("register/",views.register,name="register"),
]
