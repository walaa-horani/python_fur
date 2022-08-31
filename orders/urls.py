from  django.urls import  path
from  . import  views
urlpatterns = [

    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('remove_from_cart/<int:orderdetails_id>', views.remove_from_cart, name='remove_from_cart'),
    path('remove_fav/<int:orderdetails_id>/', views.remove_fav, name='remove_fav'),

    path('add_qty/<int:orderdetails_id>', views.add_qty, name='add_qty'),
    path('sub_qty<int:orderdetails_id>', views.sub_qty, name='sub_qty'),
    path('show_orders', views.show_orders, name='show_orders'),
    path('checkout', views.checkout, name='checkout'),


]