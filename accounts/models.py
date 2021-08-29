from django.db import models
from  django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
	# id = models.AutoField(primary_key=True) # defining a primary key type but it works from last line of settings .py
	user = models.OneToOneField(User, null=True, on_delete= models.CASCADE) #CUSTOMER CAN HAVE ONE USER AND ONE USER CAN HAVE ONE CUSTOMER. CASCADE DELETE THE RELATIONSHIP BETWEEN THE USER ON DELETE
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Tag(models.Model):
	# id = models.AutoField(primary_key=True) # defining a primary key type but it works from last line of settings .py
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			) 

	# id = models.AutoField(primary_key=True) # defining a primary key type but it works from last line of settings .py
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name

class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)

	# id = models.AutoField(primary_key=True) # defining a primary key type but it works from last line of settings .py
	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True) # field to make custom attribute search for order in customer template. then goto customer template to add this attribute 

	def __str__(self):
		return self.product.name



	
