from django.db import models

class City(models.Model):
	city_id = models.DecimalField(max_digits=10,decimal_places=0,primary_key=True)
	city_name = models.CharField(max_length=200) 
	def __str__(self):
		return str(self.city_id)+" "+self.city_name
	

class Customer(models.Model):
	u_id = models.DecimalField(max_digits=10,decimal_places=0,primary_key=True)
	u_name = models.CharField(max_length=200)
	u_mobile = models.DecimalField(max_digits=10,decimal_places=0)
	u_address = models.CharField(max_length=1000)
	u_city = models.CharField(max_length=200)
	u_email = models.EmailField(max_length=200,unique=True)
	u_password = models.CharField(max_length=200)
	u_latest_cart_id = models.DecimalField(max_digits=3,decimal_places=0)
	def __str__(self):
		return str(self.u_id)+" "+self.u_name
	
class Restaurant(models.Model):
	r_id = models.DecimalField(max_digits=10,decimal_places=0,primary_key=True)
	r_name = models.CharField(max_length=200)
	r_mobile = models.DecimalField(max_digits=10,decimal_places=0)
	r_address = models.CharField(max_length=1000)
	r_city = models.CharField(max_length=200)
	r_rating = models.DecimalField(max_digits=2,decimal_places=1)
	r_email = models.EmailField(max_length=200,unique=True)
	r_password = models.CharField(max_length=200)
	img_url = models.URLField(max_length=200)
	def __str__(self):
		return str(self.r_id)+" "+self.r_name
	
class Admin(models.Model):
	a_id = models.DecimalField(max_digits=10,decimal_places=0,primary_key=True)
	a_name = models.CharField(max_length=200)
	a_mobile = models.DecimalField(max_digits=10,decimal_places=0)
	a_address = models.CharField(max_length=1000)
	a_city = models.CharField(max_length=200)
	a_email = models.EmailField(max_length=200,unique=True)
	a_password = models.CharField(max_length=200)
	def __str__(self):
		return str(self.a_id)+" "+self.a_name
	
class Menu(models.Model):
	m_id = models.DecimalField(max_digits=5,decimal_places=0,primary_key=True)
	def __str__(self):
		return str(self.m_id)
	
class Cuisine(models.Model):
	cuisine_id = models.DecimalField(max_digits=5,decimal_places=0,primary_key=True)
	cuisine_name = models.CharField(max_length=200)
	def __str__(self):
		return str(self.cuisine_id)+" "+self.cuisine_name
	
class Restaurant_Menu(models.Model):
	rm_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	menu_id = models.ForeignKey(Menu)
	restaurant = models.OneToOneField(Restaurant)
	def __str__(self):
		return str(self.menu_id)+" "+str(self.restaurant)
	
class Item(models.Model):
	i_id = models.DecimalField(max_digits=5,decimal_places=0,primary_key=True)
	i_name = models.CharField(max_length=200)
	i_cost = models.DecimalField(max_digits=10,decimal_places=2)
	i_cuisine_id = models.ForeignKey(Cuisine,on_delete=models.CASCADE)
	img_url = models.URLField(max_length=200)
	def __str__(self):
		return str(self.i_id)+" "+self.i_name

class Menu_Item(models.Model):
	mi_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	menu_id = models.ForeignKey(Menu)
	item_id = models.ForeignKey(Item, to_field='i_id')
	
	def __str__(self):
		return str(self.item_id)
	

class Cart_Item(models.Model):
	cart_item_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	item_id = models.ForeignKey(Item)
	quantity = models.DecimalField(max_digits=3,decimal_places=0)
	net_cost = models.DecimalField(max_digits=10,decimal_places=2)
	status = models.CharField(max_length=200)
	restaurant_id = models.ForeignKey(Restaurant)
	def __str__(self):
		return str(self.cart_item_id)+" "+str(self.item_id)


class Cart(models.Model):
	cart_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	total_cost = models.DecimalField(max_digits=10,decimal_places=2)

	def __eq__(self,other):
		print "vacchindi"
		return self.cart_id==other.cart_id

	def __str__(self):
		return str(self.cart_id)+" "+str(self.total_cost)
	
class Cart_Contains(models.Model):
	cc_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	cart_id = models.ForeignKey(Cart)
	cart_item_id = models.ForeignKey(Cart_Item)
	def __str__(self):
		return str(self.cart_id)+" "+str(self.cart_item_id)
	
class Payment(models.Model):
	payment_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	net_amount = models.DecimalField(max_digits=10,decimal_places=2)
	status = models.CharField(max_length=200)

	def __str__(self):
		return str(self.payment_id)

	
class Paid_For(models.Model):
	pf_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	payment_id = models.OneToOneField(Payment)
	cart_id = models.OneToOneField(Cart)

	def __str__(self):
		return str(self.pf_id)+" "+str(self.payment_id)

	
class Pay(models.Model):
	p_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
	payment_id = models.OneToOneField(Payment)

	def __str__(self):
		return str(self.p_id)+" "+str(self.customer_id)+" "+str(self.payment_id)
	
class Order(models.Model):
	order_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	total_cost = models.DecimalField(max_digits=10,decimal_places=2)
	order_status = models.CharField(max_length=200)

	def __str__(self):
		return str(self.order_id)+" "+self.order_status

	
class Restaurant_Order(models.Model):
	ro_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	restaurant_id = models.ForeignKey(Restaurant)
	order_id = models.ForeignKey(Order)
	cart_item_id = models.ForeignKey(Cart_Item)

	def __str__(self):
		return str(self.ro_id)+" "+str(self.restaurant_id)+" "+str(self.cart_item_id)+" "+str(self.order_id)

class User_Cart(models.Model):
	uc_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	user_id = models.ForeignKey(Customer)
	cart_id = models.ForeignKey(Cart)

	def __str__(self):
		return str(self.user_id)+" "+str(self.cart_id)

class Cart_Item_Order(models.Model):
	cio_id = models.DecimalField(max_digits=3,decimal_places=0,primary_key=True)
	cart_item_id = models.ForeignKey(Cart_Item)
	order_id = models.ForeignKey(Order)

	def __str__(self):
		return str(self.cart_item_id)+" "+str(self.order_id)