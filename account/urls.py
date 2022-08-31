from  django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/' ,views.signup,name='signup'),

    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('favourite_list', views.favourite_list, name='favourite_list'),
    path('product_favourite/<int:pro_id>',views.product_favourite,name='product_favourite'),
    path('change_password/',auth_views.PasswordChangeView.as_view(template_name='account/change_password.html'),name='change_password'),
    path('password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),name='password_change_done'),
    path('update_profile/',views.UserUpdateView.as_view(),name='update_profile'),
    path('remove_favourite/<slug:slug>/' ,views.remove_fav,name='remove_fav'),
    
    

]