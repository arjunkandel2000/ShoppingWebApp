from django import forms
from django.shortcuts import render, redirect 
from django.http import HttpResponse, request
from django.forms import inlineformset_factory #for making inline froms in search form, order_form etc
from django.contrib.auth.forms import UserCreationForm  #importing login forms. django provides the forms we donot need to create it
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #log in required to access the page.
from django.contrib.auth.models import Group #import the group model
from django.contrib import messages #sending one time messege 
# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm # createuserform imported from forms.py and the form below in registerPage is repalced as CreateUserForm
from .filters import OrderFilter
from accounts.decorators import  unauthenticated_user,  allowed_users,admin_only


def registerPage(request):
	if request.user.is_authenticated: #if user is logged in he cannot goto login page withouth logging out
		return redirect('home')
	else:
		form = CreateUserForm() #rendering registration form. this is django created form but in forms.py there is userCreated form
		#processing the data
		if request.method == 'POST': 
			form = CreateUserForm(request.POST) # throwing the data in to the form(username and password)
			if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username') #getting username from the form
				group = Group.objects.get(name= 'customer') #when user signs up user automatiically set to the customer group
				user.groups.add(group) # user is added to cusstomer group name
				messages.success(request, 'Account was created for ' + username + '.') #see documentation. if there is already a account this messege will be dispalyed and redirected to login page
				return redirect('login')	
	context = {'form': form}  #passing the form to our template
	return render(request, 'accounts/register.html', context)


	
@unauthenticated_user #this is builtin django decorator. this passes the loginPage view function to unauthenticated_user in user.html as an agrgument
def loginPage(request):
	# if request.user.is_authenticated: #if user is logged in he cannot goto login page withouth logging out
	# 	return redirect('home')
	# else:
	if request.method == 'POST': # checks if the method is posts
		username = request.POST.get('username') #grabs username from login page
		password = request.POST.get('password')

			#checking if that username and password in the database i.e. authentication
		user = authenticate(request, username= username, password= password ) #second username is username got from above request method

		if user is not None: #if username or password exists
			login(request,user)
			return redirect('home')
		else: #if user name or passoword doesnot exists
			messages.info(request,'Username or Password is incorrect.')
	context = {} 
	return render(request, 'accounts/login.html', context)

	


def logoutUser(request):
	logout(request)
	return redirect('login') #after logout it will redirect us to log in page


@login_required(login_url='login') #it is set to every page which are only to be accessible after logs in. otherwise user is redirected to only loginPage
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)


def userPage(request):
	context={}
	return render(request,'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset= orders) # queries all the orders and filters according to the search
	orders = myFilter.qs # placing the filtered data into new variable orders and now you can search

	context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)
