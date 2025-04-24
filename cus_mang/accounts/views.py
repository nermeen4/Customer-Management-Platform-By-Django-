from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms  import *
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group




#Register endpoints:
@unauthenticated_user
def registerPage(request):
    form= RegisterForm()
    if request.method == "POST":
        form =RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            username= form.cleaned_data.get('username')
            group = Group.objects.get(name='customers')
            user.groups.add(group)
            Customer.objects.create(
                 user=user,
             )
            
            messages.success(request,  ' Account created for ' +  username)
            return redirect('login_page')
            
    context={'register_form':form}
    return render(request, 'accounts/register.html', context)



#Login endpoints:
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user=authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username Or Password is incorrect') 
    context={}
    return render(request, 'accounts/login.html', context)




# logout endpoint
def logoutUser(request):
    logout(request)
    return redirect('login_page')



# User profile endpoint
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['customers'])
def userPage(request):
    orders= request.user.customer.order_set.all()
    total_orders=orders.count()
    deliverd_orders=orders.filter(status='Deliverd').count()
    pending_orders=orders.filter(status='Pending').count()
    context={'cus_orders':orders,'total_orders':total_orders, 'deliverd_orders':deliverd_orders,'pending_orders':pending_orders}
    return render(request, 'accounts/user.html', context)




# user settings endpoint
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['customers', 'admins'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance= customer)
     
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    
    context={'form': form}
    return render(request, 'accounts/account_settings.html', context)






# Default page endpoints:
@login_required(login_url='login_page')
@admin_only
def dashboard(request):
    orders= Order.objects.all()
    customers= Customer.objects.all()
    total_orders=orders.count()
    deliverd_orders=orders.filter(status='Deliverd').count()
    pending_orders=orders.filter(status='Pending').count()
    context={'list_of_orders':orders, 'list_of_customers':customers,
    'total_orders':total_orders, 'deliverd_orders':deliverd_orders,'pending_orders':pending_orders}
    return render(request, 'accounts/dashboard.html', context)



# Products endpoints:
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins'])
def products(request):
    products= Product.objects.all()
    return render(request,'accounts/products.html',{'list_of_product':products})



#Curtomers endpoints:(get)
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins'])
def customers(request, pk):
    customer= Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    order_count= orders.count()
    
    myfilter= OrderFilter(request.GET, queryset=orders)
    orders= myfilter.qs
    context={'customer_id':customer,'cus_orders':orders, 'order_count':order_count, 'myfilter':myfilter}
    return render(request, 'accounts/customers.html', context)


# post function:
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins'])
def createCustomer(request):
    form2= CustomerForm()
    if request.method == 'POST':
        form2 = CustomerForm(request.POST)
        if form2.is_valid():
            form2.save()
            return redirect('/')
        
    context={'customer_form':form2}
    return render(request, 'accounts/customer_form.html', context)




# Orders endpoints: (post)
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins'])
def createOrder(request,pk):
    OrderFormSet= inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer= Customer.objects.get(id=pk)
    formset= OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method =='POST':
        formset= OrderFormSet(request.POST, instance=customer)
        #form= OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')       
    context={'formset':formset}
    return render(request, 'accounts/order_form.html', context)


# Put function 
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins'])
def updateOrder(request, pk):
    order=Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method =='POST':
        form= OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
            
    context={'form':form}
    return render (request, 'accounts/order_form.html', context)


# Delete function
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins'])
def deleteOrder(request, pk):
    order=Order.objects.get(id=pk)
    
    if request.method=="POST":
        order.delete()
        return redirect('/')
    
    context={'item':order}
    return render(request, 'accounts/delete.html', context)



