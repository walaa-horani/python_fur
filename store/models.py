from audioop import reverse
from dataclasses import field

from django.db import models
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models


from django.utils.safestring import mark_safe
# Create your models here.
class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=150, unique=True)
   
    slug = models.SlugField(null=True, blank=True)



    def __str__(self):
        return self.title
    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug':self.slug})    


    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])   

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='img')
    Manufacturer =  models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = RichTextField()
    price = models.IntegerField()
    dis_price = models.IntegerField(default=0)
    favourite = models.ManyToManyField(User,related_name='favourite', blank=True)
    slug = models.SlugField(null=True, blank=True)  
    amout= models.IntegerField()
    likes= models.ManyToManyField(User,related_name='likes', blank=True)
    
    
    popular = models.BooleanField()
    featured= models.BooleanField()
    new= models.BooleanField()

    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)  
        

    
    

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=250)
    image = models.ImageField(upload_to='photos')

    def __str__(self):
        return self.title  




class Comment(models.Model):
    STATUS = (
        ('New','New'),
        ('True','True'),
        ('False','False')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000,blank=True ) 
    rate = models.FloatField(default=1) 
    subject = models.CharField(max_length=400,blank=True ) 
    ip =  models.CharField(max_length=400 )   
    status= models.CharField(max_length=10, default='new')   

    def __str__(self):
        return self.subject



class CommentForm(ModelForm):
    class Meta:
        model = Comment  

        fields = ['subject','comment','rate']    


       
class ContactMessage(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    subject= models.CharField(max_length=50)
    message=models.TextField(max_length=450)
    ip=models.CharField(max_length=20)
    note=models.CharField(max_length=320)


    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage  
        fields = ['name','email','subject','message'] 
        widgets = {
            'name': TextInput(attrs={'class':'form-control','placeholder':'name and surname'}),
            'subject': TextInput(attrs={'class':'form-control','placeholder':'subject'}),
            'email': TextInput(attrs={'class':'form-control','placeholder':'email'}),
            'message': Textarea(attrs={'class':'form-control','placeholder':'message'}),
        }        