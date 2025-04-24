from django.db import models
from django.contrib.auth.models import User

# table of customers
# null= true to let u don't write what u want to 

class Customer(models.Model):
    # one to one relation between user and customer
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email= models.CharField(max_length=100, null=True)
    phone= models.CharField(max_length=200, null= True)
    profile_pic=models.ImageField(null=True, blank=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    
    
# this function used to data representation to show us the name of customer we create instead of customer object

    def __str__(self):
       return self.name if self.name else "Unnamed Customer"
   

class Tag(models.Model):
    name= models.CharField(max_length=200, null=True)
    
    def __str__(self):
       return self.name
   
    
   
   
   
class Product (models.Model):
    CATEGORY=(
        
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    
    name= models.CharField(max_length=200, null=True)
    price= models.FloatField(null=True)
    category= models.CharField(max_length=200, null=True, choices=CATEGORY)
    describtion= models.CharField(max_length=200, null=True, blank=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    tags=models.ManyToManyField(Tag)
    
    def __str__(self):
       return self.name
   

   
   
class Order(models.Model):
    STATUS=(
        
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Deliverd', 'Deliverd'),
    )
    
    customer=models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product=models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created=models.DateTimeField(null=True, auto_now_add=True)
    status=models.CharField( max_length=200,null=True, choices=STATUS)
    note=models.CharField(max_length=1000, null=True)
    
    def __str__(self):
        return self.product.name
       #return f'{self.customer}, {self.product}'
   