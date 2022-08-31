
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store,name='store'),
    path('about/', views.about,name='about'),
    path('category/<int:id>/<slug:slug>',views.category_products,name='category_products'),
    path('<int:id>/<slug:slug>',views.product_details,name='product_details'),
    path('addcomment/<slug:slug>',views.addcomment,name='addcomment'),
    path('search/',views.search,name='search'),
    path('popular/',views.popular,name='popular'),
    path('featured/',views.featured,name='featured'),
    path('autocomplete/',views.autocomplete,name='autocomplete'),
    path('contact_us/', views.contact_us,name='contact_us'),
    path('like/<slug:slug>',views.like,name="like_post")

    
]