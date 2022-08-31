from django.db.models import fields
from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from  .forms import  SignUpForm
from store.models import Product, Category
from  django.contrib.auth.forms import UserCreationForm
# Create your views here.
def signup(request):
    
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            
            user = form.save()
            auth_login(request,user)
            return  redirect('store')
    return render(request,'account/signup.html',{'form':form})


@login_required
def favourite_list(request):
    category = Category.objects.all()
    context = None
    user = request.user
    pro= user.favourite.all()
    context = {
        'products': pro,
        'category':category
    }

    return  render(request,'store/favourite_list.html', context )

def remove_fav(request,slug):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav= get_object_or_404(Product, slug=slug)
        fav = False
        if pro_fav.favourite.filter(id=request.user.id).exists():
            pro_fav.delete()
            fav = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'),{'fav':fav})
        

def product_favourite(request, pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav= get_object_or_404(Product, id=pro_id)
        if pro_fav.favourite.filter(id=request.user.id).exists():

            messages.success(request, 'prodcut  already  added to wishlist')

        else:
            pro_fav.favourite.add(request.user)
            messages.success(request,'prodcut has been added to wishlist')
    else:
        messages.error(request,'please log in to add it to favourites')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


 

class UserUpdateView(UpdateView):
   
            
    
    fields = ('first_name', 'last_name','email','username')
    template_name = 'account/update_profile.html'
    success_url =  reverse_lazy('update_profile')
   

    def get_object(self):
         return self.request.user
   




