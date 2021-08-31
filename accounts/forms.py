from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Customer, Order


def CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = [ 'user']

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'

class CreateUserForm(UserCreationForm): #this form inherits from usercreationform. here we create the replica of it and we customize that form
	class Meta:
		model = User #model is User so we need to import it
		fields= ['username','email', 'password1', 'password2'] #from dcumentation of django
