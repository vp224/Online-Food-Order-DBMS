from django.contrib import admin
from .models import City
from .models import Customer
from .models import Restaurant
from .models import Admin
from .models import Menu
from .models import Cuisine
from .models import Restaurant_Menu
from .models import Item
from .models import Menu_Item
from .models import Cart_Item
from .models import Cart
from .models import Cart_Contains
from .models import Payment
from .models import Paid_For
from .models import Pay
from .models import Order
from .models import Restaurant_Order



admin.site.register(City)
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(Admin)
admin.site.register(Menu)
admin.site.register(Cuisine)
admin.site.register(Restaurant_Menu)
admin.site.register(Item)
admin.site.register(Menu_Item)
admin.site.register(Cart_Item)
admin.site.register(Cart)
admin.site.register(Cart_Contains)
admin.site.register(Payment)
admin.site.register(Paid_For)
admin.site.register(Pay)
admin.site.register(Order)
admin.site.register(Restaurant_Order)
# Register your models here.
