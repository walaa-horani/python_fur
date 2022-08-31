from itertools import product
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render,reverse
from . models import Category,Product,Images,CommentForm, Comment,ContactForm,ContactMessage
from django.contrib import messages
from django.contrib.auth.models import User
from store.forms import SearchForm
import json

# Create your views here.
def store(request):
    category = Category.objects.all()
    product = Product.objects.all()
    page = 'store'

    comment =Comment.objects.all()
    
    
    return render(request,'store/store.html', {'category':category,'product':product,'page':page,'comment':comment})



def about(request):
    category = Category.objects.all()
    product = Product.objects.all()
    
    return render(request,'store/about.html', {'category':category,'product':product})    


def popular(request):
    category = Category.objects.all()
    product = Product.objects.all()
    
    return render(request,'store/popular.html', {'category':category,'product':product})  

def contact_us(request):
    if request.method == 'POST':
     form = ContactForm(request.POST)
     if form.is_valid():
       
         data = ContactMessage()
         data.name = form.cleaned_data['name']
         data.email = form.cleaned_data['email']
         data.subject = form.cleaned_data['subject']
         data.message = form.cleaned_data['message']
         data.ip = request.META.get('REMOTE_ADDR')
         
         data.save()
         messages.success(request,'your massege has been sent')
         return HttpResponseRedirect('/contact_us/')

    else:

     

       
   
    
     form = ContactForm()
    
   
    return render(request,'store/contact_us.html', {'form':form})  

def featured(request):
    category = Category.objects.all()
    product = Product.objects.all()
    
    return render(request,'store/featured.html', {'category':category,'product':product})  

def category_products(request, id, slug):
    category = Category.objects.all()
    products = Product.objects.filter(category=id)


    return render(request, 'store/category_products.html', {'category': category, 'products': products})   

def like(request,slug):
    product= get_object_or_404(Product,slug=slug)
    
    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
       
    else:    
        product.likes.add(request.user)
      
    return HttpResponseRedirect(reverse('product_details', args=[str(slug)]))

def product_details(request,id, slug):
    category = Category.objects.all()
    products = Product.objects.get(slug=slug)
    photos = Images.objects.filter(product=products)
    comments = Comment.objects.filter(product=id)
    stuff = get_object_or_404(Product, slug=slug)
    total_likes = stuff.total_likes()
    liked = False
    if stuff.likes.filter(id=request.user.id).exists():
        liked=True


   
    
   
    return render(request, 'store/product_details.html', {'category': category, 'products': products, 'photos': photos, 'comments':comments,'total_likes':total_likes,'liked':liked,'stuff':stuff})    


def addcomment(request,slug):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
         data = Comment()
         data.subject = form.cleaned_data['subject']
         data.comment = form.cleaned_data['comment']
         data.ip = request.META.get('REMOTE_ADDR')
         data.product=Product.objects.get(slug=slug)
         current_user = request.user.id
         data.rate = form.cleaned_data['rate']
         data.user =User.objects.get(id=current_user)
         data.save()
         messages.success(request,'thanks for your review ')
   
    else:
        messages.error(request,'please add your review ')
    


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        
    
            
def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query= form.cleaned_data['query']
            cat =form.cleaned_data['cat']

            if cat==0:
                products= Product.objects.filter(title__icontains=query) 
            else:
                products = Product.objects.filter(title__icontains=query,category_id=cat)

            category = Category.objects.all() 
            context = {'products':products,
                       'category':category     
            }         
            return render(request,'store/search.html', context)

    return HttpResponseRedirect('/')  



def autocomplete(request):
    if 'term' in request.GET:
        qs= Product.objects.filter(title__icontains=request.GET.get('term'))   
        titles = list()
        for product in qs:
            titles.append(product.title)
        return JsonResponse(titles,safe=False)

    return render(request,'store/search.html')          