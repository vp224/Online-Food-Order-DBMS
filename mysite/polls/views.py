from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render

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
from .models import User_Cart
from .models import Restaurant_Order
from .models import Cart_Item_Order

def index(request):
    template = loader.get_template('polls/signup.html')
    request.session['current_user']=str(0)
    request.session['current_rest']=str(0)
    request.session['current_admin']=str(0)
    context={
    	'val':0,
    }
    #for u in User.objects.all():
    #	print u
    return render(request, 'polls/signup.html',context)

def detail(request):
    a=request.POST['fname']
    b=int(request.POST['phone'])
    c=request.POST['optradio']
    if c=="Customer" :
        u = Customer()
        if Customer.objects.all().count() > 0 :
            u.u_id = Customer.objects.latest('u_id').u_id + 1
        else : 
            u.u_id = 1
        u.u_name=a
        u.u_mobile=b
        u.u_address=request.POST['address']
        u.u_city=request.POST['city']
        u.u_email=request.POST['email']
        u.u_password=request.POST['password']
        u.latest_cart_id = 0
        u.save()
    elif c=="Restaurant":
        r = Restaurant()
        if Restaurant.objects.all().count() > 0 :
            r.r_id = Restaurant.objects.latest('r_id').r_id + 1
        else : 
            r.r_id = 1
        r.r_name = a
        r.r_mobile = b
        r.r_address=request.POST['address']
        r.r_city=request.POST['city']
        u.r_email=request.POST['email']
        r.r_password=request.POST['password']
        r.rating = 3
        r.save()

    for u in Customer.objects.all():
        print str(u.u_id)+" "+u.u_name
    context={
    	'val':1,
    }
    return render(request, 'polls/signup.html',context)
    
def login_check(request):
	#user_object = get_object_or_404(User, u_email=request.POST['email'],u_password=request.POST['password'])
    if int(request.session.get('current_user','0')) == 0 :
        try:
            c = Customer.objects.get(u_email = request.POST['email'])
            request.session['current_user']=str(c.u_id)
            request.session['current_rest']=str(0)
            request.session['current_admin']=str(0)
            cur_user = Customer.objects.get(pk=c.u_id)
            if cur_user.u_latest_cart_id:
                cart_items_count=0
                cart_items = Cart_Contains.objects.all()
                for lol in cart_items:
                    if lol.cart_id.cart_id==cur_user.u_latest_cart_id:
                        cart_items_count = cart_items_count+lol.cart_item_id.quantity
        
            else:
                print "lolmaxx"
                cart_items_count = 0

            city_list = City.objects.all()
            context = {
            'cart_items_count':cart_items_count,
            'city_list':city_list,
            }
            return render(request, 'polls/search.html',context)
        except Exception as e:
            print e
            try:
                if int(request.session.get('current_rest','0'))==0 :
                    r = Restaurant.objects.get(r_email=request.POST['email'])
                    request.session['current_user']=str(0)
                    request.session['current_rest']=str(r.r_id)
                    request.session['current_admin']=str(0)
                else :
                    r = Restaurant.objects.get(pk=int(request.session.get('current_rest','0')))

                ro = Restaurant_Order.objects.all()
                all_orders = []
                for ri in ro:
                    if ri.restaurant_id.r_id==r.r_id:
                        order = ri.order_id
                        cart_item = ri.cart_item_id
                        cart_contains = Cart_Contains.objects.all()
                        if cart_item.status!="delivered":
                            for cc in cart_contains:
                                if cc.cart_item_id.cart_item_id==cart_item.cart_item_id:
                                    cart = cc.cart_id
                                    user_cart = User_Cart.objects.all()
                                    for uc in user_cart:
                                        if uc.cart_id.cart_id==cc.cart_id.cart_id:
                                            cust = Customer.objects.get(pk=uc.user_id.u_id)
                                            all_orders.append({'order':order,'cust':cust,'cart_item':cart_item})

                context = {
                    'r':r,
                    'all_orders':all_orders,
                }
                return render(request, 'polls/restaurant_orders.html',context)
            except Exception as e1:
                print e1
                if int(request.session.get('current_admin','0'))==0 :
                    a = Admin.objects.get(a_email=request.POST['email'])
                    request.session['current_user']=str(0)
                    request.session['current_rest']=str(0)
                    request.session['current_admin']=str(a.a_id)
                else :
                    a = Admin.objects.get(pk=int(request.session.get('current_admin','0')))


    else :
        cur_user = Customer.objects.get(pk=int(request.session.get('current_user','0')))
        if cur_user.u_latest_cart_id:
            cart_items_count=0
            cart_items = Cart_Contains.objects.all()
            for lol in cart_items:
                if lol.cart_id.cart_id==cur_user.u_latest_cart_id:
                    cart_items_count = cart_items_count+lol.cart_item_id.quantity
        
        else:
            print "lolmaxx"
            cart_items_count = 0
        city_list = City.objects.all()
        context = {
        'cart_items_count':cart_items_count,
        'city_list':city_list
        }
        return render(request, 'polls/search.html',context)
            
	
def vote(request, question_id):
    return HttpResponse("You're voting on question")

def rest_by_city(request,city):
    rest_list = Restaurant.objects.all().filter(r_city=City.objects.get(pk=city).city_name)
    cuisine_list = Cuisine.objects.all()
    cur_user = Customer.objects.get(pk=int(request.session.get('current_user','0')))
    if cur_user.u_latest_cart_id:
        cart_items_count=0
        cart_items = Cart_Contains.objects.all()
        for lol in cart_items:
            if lol.cart_id.cart_id==cur_user.u_latest_cart_id:
                cart_items_count = cart_items_count+lol.cart_item_id.quantity
        
    else:
        cart_items_count = 0
    
    context ={
        'rest_list':rest_list,
        'cuisine_list':cuisine_list,
        'cart_items_count':cart_items_count,
    }
    return render(request, 'polls/listing.html',context)

def food_by_rest(request,rest_id):
    
    menu_id = Restaurant_Menu.objects.get(restaurant=rest_id)
    item_id_list = Menu_Item.objects.all().filter(menu_id=menu_id.menu_id)
    item_list = []
    for i in item_id_list:
        item_list.append(Item.objects.get(pk=i.item_id.i_id))
    rest_obj = Restaurant.objects.get(pk=rest_id)

    cur_user = Customer.objects.get(pk=int(request.session.get('current_user','0')))
    if cur_user.u_latest_cart_id:
        cart_items_count=0
        cart_items = Cart_Contains.objects.all()
        for lol in cart_items:
            if lol.cart_id.cart_id==cur_user.u_latest_cart_id:
                cart_items_count = cart_items_count+lol.cart_item_id.quantity
        
    else:
        cart_items_count = 0
    
    context = {
        'item_list':item_list,
        'rest_obj':rest_obj,
        'added':0,
        'cart_items_count':cart_items_count,
    }
    return render(request, 'polls/restaurant.html',context)

def added(request,rest_id,it_id):
    menu_id = Restaurant_Menu.objects.get(restaurant=rest_id)
    item_id_list = Menu_Item.objects.all().filter(menu_id=menu_id.menu_id)
    item_list = []
    for i in item_id_list:
        item_list.append(Item.objects.get(pk=i.item_id.i_id))
    rest_obj = Restaurant.objects.get(pk=rest_id)
    
    ct = Cart_Item()
    if Cart_Item.objects.all().count() > 0 :
        ct.cart_item_id = Cart_Item.objects.latest('cart_item_id').cart_item_id+1
    else :
        ct.cart_item_id = 1
    ct.item_id = Item.objects.get(pk=it_id)
    ct.quantity = 1
    ct.net_cost = Item.objects.get(pk=it_id).i_cost
    ct.status = "ordered"
    ct.restaurant_id = rest_obj
    ct.save()

    test = Customer.objects.get(u_id=int(request.session.get('current_user','0')))
    if test.u_latest_cart_id!=0:
        present_cart = Cart.objects.get(pk=Customer.objects.get(u_id=int(request.session.get('current_user','0'))).u_latest_cart_id)
        found=0
        for f in Cart_Contains.objects.all():
            print str(f.cart_id.cart_id)+" "+str(f.cart_item_id.item_id.i_id)
            if f.cart_id.cart_id==test.u_latest_cart_id :
                if str(f.cart_item_id.item_id.i_id)==str(it_id) :
                    found=1
                    f.cart_item_id.quantity = f.cart_item_id.quantity+1
                    f.cart_item_id.save()
                    break
                
        if found==0:
            cc = Cart_Contains()
            if Cart_Contains.objects.all().count() > 0:
                cc.cc_id = Cart_Contains.objects.latest('cc_id').cc_id +1
            else : 
                cc.cc_id = 1
            cc.cart_id = Cart.objects.get(pk=test.u_latest_cart_id)
            cc.cart_item_id = ct
            cc.save()
        
    else :
        c = Cart()
        if Cart.objects.all().count() > 0 :
            c.cart_id = Cart.objects.latest('cart_id').cart_id +1
        else :
            c.cart_id = 1
        c.total_cost = 0
        c.save()

        uc = User_Cart()
        if User_Cart.objects.all().count() > 0 :
            uc.uc_id = User_Cart.objects.latest('uc_id').uc_id +1
        else : 
            uc.uc_id = 1
        uc.user_id = Customer.objects.get(u_id=int(request.session.get('current_user','0')))
        uc.cart_id = c
        uc.save()

        cc = Cart_Contains()
        if Cart_Contains.objects.all().count() > 0 :
            cc.cc_id = Cart_Contains.objects.latest('cc_id').cc_id +1
        else : 
            cc.cc_id = 1
        cc.cart_id = c
        cc.cart_item_id = ct
        cc.save()

        cur_user = Customer.objects.get(u_id=int(request.session.get('current_user','0')))
        cur_user.u_latest_cart_id = c.cart_id
        cur_user.save()

    cur_user = Customer.objects.get(pk=int(request.session.get('current_user','0')))
    if cur_user.u_latest_cart_id:
        cart_items_count=0
        cart_items = Cart_Contains.objects.all()
        for lol in cart_items:
            if lol.cart_id.cart_id==cur_user.u_latest_cart_id:
                cart_items_count = cart_items_count+lol.cart_item_id.quantity
        
    else:
        cart_items_count = 0
    
    context = {
        'item_list':item_list,
        'rest_obj':rest_obj,
        'added':1,
        'cart_items_count':cart_items_count,
    }
    return render(request, 'polls/restaurant.html',context)    

def cart_checkout(request):
    cur_user = Customer.objects.get(pk=int(request.session.get('current_user','0')))
    if cur_user.u_latest_cart_id!=0 :
        latest_cart = Cart.objects.get(pk=cur_user.u_latest_cart_id)
    else :
        latest_cart = 0
    cart_contains = []
    cc_all = Cart_Contains.objects.all()
    tot_cost = 0

    if cur_user.u_latest_cart_id!=0 :
        for cc in cc_all:
            if cc.cart_id.cart_id==latest_cart.cart_id:
                it1 = Item.objects.get(pk=cc.cart_item_id.item_id.i_id)
                it2 = Cart_Item.objects.get(pk=cc.cart_item_id.cart_item_id)
                it3 = it1.i_cost*it2.quantity
                tot_cost = tot_cost + it3
                cart_contains.append({'item':it1,'quan':it2,'tot':it3})

    charges = tot_cost+100
    context = {
        'cart_contains':cart_contains,
        'tot_cost':tot_cost,
        'charges':charges,
    }  
    return render(request, 'polls/order-part1.html',context)    


def confirm_cart(request):



    cur_user = Customer.objects.get(pk=int(request.session.get('current_user','0')))
    latest_cart = Cart.objects.get(pk=cur_user.u_latest_cart_id)
    cart_contains = []
    cc_all = Cart_Contains.objects.all()
    tot_cost = 0
    for cc in cc_all:
        if cc.cart_id.cart_id==latest_cart.cart_id:
            it1 = Item.objects.get(pk=cc.cart_item_id.item_id.i_id)
            it2 = Cart_Item.objects.get(pk=cc.cart_item_id.cart_item_id)
            it3 = it1.i_cost*it2.quantity
            tot_cost = tot_cost + it3
            cart_contains.append({'item':it1,'quan':it2,'tot':it3})

    charges = tot_cost+100
    context = {
        'cart_contains':cart_contains,
        'tot_cost':tot_cost,
        'charges':charges,
    }  
    return render(request, 'polls/order-part2.html',context)    

def make_payment(request):
    

    cur_user = Customer.objects.get(pk=int(request.session.get('current_user','0')))
    latest_cart = Cart.objects.get(pk=cur_user.u_latest_cart_id)
    cart_contains = []
    cc_all = Cart_Contains.objects.all()
    tot_cost = 0
    for cc in cc_all:
        if cc.cart_id.cart_id==latest_cart.cart_id:
            it1 = Item.objects.get(pk=cc.cart_item_id.item_id.i_id)
            it2 = Cart_Item.objects.get(pk=cc.cart_item_id.cart_item_id)
            it3 = it1.i_cost*it2.quantity
            tot_cost = tot_cost + it3
            
            order = Order()
            if Order.objects.all().count() > 0 :
                order.order_id = Order.objects.latest('order_id').order_id+1
            else :
                order.order_id = 1  
            order.total_cost = it3
            order.order_status = "preparing"
            order.save()
            #print order 
            cart_item_order = Cart_Item_Order()
            if Cart_Item_Order.objects.all().count() > 0 :
                cart_item_order.cio_id = Cart_Item_Order.objects.latest('cio_id').cio_id + 1
            else : 
                cart_item_order.cio_id = 1
            cart_item_order.cart_item_id = cc.cart_item_id
            cart_item_order.order_id = order
            cart_item_order.save()

            restaurant_order = Restaurant_Order()
            if Restaurant_Order.objects.all().count() > 0 :
                restaurant_order.ro_id = Restaurant_Order.objects.latest('ro_id').ro_id+1
            else : 
                restaurant_order.ro_id = 1
            restaurant_order.restaurant_id = cc.cart_item_id.restaurant_id 
            restaurant_order.order_id = order
            restaurant_order.cart_item_id = cc.cart_item_id
            restaurant_order.save()
            #print restaurant_order
            
            cart_contains.append({'item':it1,'quan':it2,'tot':it3})

    charges = tot_cost+100

    payment = Payment()
    if Payment.objects.all().count() > 0 : 
        payment.payment_id = Payment.objects.latest('payment_id').payment_id+1
    else : 
        payment.payment_id = 1
    payment.net_amount = charges
    payment.status = "paid"
    payment.save()
    
    paid_for = Paid_For()
    if Paid_For.objects.all().count() > 0 :
        paid_for.pf_id = Paid_For.objects.latest('pf_id').pf_id+1
    else :
        paid_for.pf_id = 1
    paid_for.payment_id = payment
    paid_for.cart_id = latest_cart
    paid_for.save()

    pay = Pay()
    if Pay.objects.all().count() > 0 : 
        pay.p_id = Pay.objects.latest('p_id').p_id +1
    else :
        pay.p_id = 1
    pay.customer_id = cur_user
    pay.payment_id = payment
    pay.save()

    cur_user.u_latest_cart_id = 0
    cur_user.save()

    context = {
        'cart_contains':cart_contains,
        'tot_cost':tot_cost,
        'charges':charges,
        'payment':payment
    }
    return render(request, 'polls/order-part3.html',context)
    

def remove(request,cc_id):
    cart_item = Cart_Item.objects.get(pk=cc_id)
    cart_item.delete()

    cur_user = Customer.objects.get(pk=int(request.session.get('current_user','0')))
    if cur_user.u_latest_cart_id!=0 :
        latest_cart = Cart.objects.get(pk=cur_user.u_latest_cart_id)
    else :
        latest_cart = 0
    cart_contains = []
    cc_all = Cart_Contains.objects.all()
    tot_cost = 0

    if cur_user.u_latest_cart_id!=0 :
        for cc in cc_all:
            if cc.cart_id.cart_id==latest_cart.cart_id:
                it1 = Item.objects.get(pk=cc.cart_item_id.item_id.i_id)
                it2 = Cart_Item.objects.get(pk=cc.cart_item_id.cart_item_id)
                it3 = it1.i_cost*it2.quantity
                tot_cost = tot_cost + it3
                cart_contains.append({'item':it1,'quan':it2,'tot':it3})

    charges = tot_cost+100
    context = {
        'cart_contains':cart_contains,
        'tot_cost':tot_cost,
        'charges':charges,
    }  
    return render(request, 'polls/order-part1.html',context)    

def track(request):
    all_carts = []
    cur_user = Customer.objects.get(pk=int(request.session.get('current_user','0')))
    all_paid_for = Paid_For.objects.all()
    pays = Pay.objects.all()
    for p in pays:
        if p.customer_id.u_id==int(request.session.get('current_user','0')):
            for pp in all_paid_for:
                if pp.payment_id.payment_id==p.payment_id.payment_id:
                    all_carts.append(Cart.objects.get(pk=pp.cart_id.cart_id))
    all_carts.reverse()
    st = []
    for a in all_carts:
        payment = 0
        for aa in all_paid_for:
            if aa.cart_id.cart_id==a.cart_id:
                payment = aa.payment_id


        cart_contains = []
        cc_all = Cart_Contains.objects.all()
        tot_cost = 0

        for cc in cc_all:
            if cc.cart_id.cart_id==a.cart_id:
                it1 = Item.objects.get(pk=cc.cart_item_id.item_id.i_id)
                it2 = Cart_Item.objects.get(pk=cc.cart_item_id.cart_item_id)
                it3 = it1.i_cost*it2.quantity
                tot_cost = tot_cost + it3
                cart_contains.append({'item':it1,'quan':it2,'tot':it3})

        charges = tot_cost+100
        st.append({'cart':a,'payment':payment,'cart_contains':cart_contains,'tot_cost':tot_cost,'charges':charges})
    
    context = {
        'st':st,
    }

    return render(request, 'polls/track.html',context)

def cook(request,order,cart_item):

    curr_or = Order.objects.get(pk=order)
    curr_ci = Cart_Item.objects.get(pk=cart_item)

    curr_or.status = "cooking"
    curr_or.save()

    curr_ci.status = "cooking"
    curr_ci.save()

    r = Restaurant.objects.get(pk=int(request.session.get('current_rest','0')))
    ro = Restaurant_Order.objects.all()
    all_orders = []
    for ri in ro:
        if ri.restaurant_id.r_id==r.r_id:
            order = ri.order_id
            cart_item = ri.cart_item_id
            cart_contains = Cart_Contains.objects.all()
            if cart_item.status!="delivered":
                for cc in cart_contains:
                    if cc.cart_item_id.cart_item_id==cart_item.cart_item_id:
                        cart = cc.cart_id
                        user_cart = User_Cart.objects.all()
                        for uc in user_cart:
                            if uc.cart_id.cart_id==cc.cart_id.cart_id:
                                cust = Customer.objects.get(pk=uc.user_id.u_id)
                                all_orders.append({'order':order,'cust':cust,'cart_item':cart_item})

    context = {
        'r':r,
        'all_orders':all_orders,
    }
    return render(request, 'polls/restaurant_orders.html',context)

def deliver(request,order,cart_item):

    curr_or = Order.objects.get(pk=order)
    curr_ci = Cart_Item.objects.get(pk=cart_item)

    curr_or.status = "delivering"
    curr_or.save()

    curr_ci.status = "delivering"
    curr_ci.save()

    r = Restaurant.objects.get(pk=int(request.session.get('current_rest','0')))
    ro = Restaurant_Order.objects.all()
    all_orders = []
    for ri in ro:
        if ri.restaurant_id.r_id==r.r_id:
            order = ri.order_id
            cart_item = ri.cart_item_id
            cart_contains = Cart_Contains.objects.all()
            if cart_item.status!="delivered":
                for cc in cart_contains:
                    if cc.cart_item_id.cart_item_id==cart_item.cart_item_id:
                        cart = cc.cart_id
                        user_cart = User_Cart.objects.all()
                        for uc in user_cart:
                            if uc.cart_id.cart_id==cc.cart_id.cart_id:
                                cust = Customer.objects.get(pk=uc.user_id.u_id)
                                all_orders.append({'order':order,'cust':cust,'cart_item':cart_item})

    context = {
        'r':r,
        'all_orders':all_orders,
    }
    return render(request, 'polls/restaurant_orders.html',context)

def done(request,order,cart_item):

    curr_or = Order.objects.get(pk=order)
    curr_ci = Cart_Item.objects.get(pk=cart_item)

    curr_or.status = "delivered"
    curr_or.save()

    curr_ci.status = "delivered"
    curr_ci.save()

    r = Restaurant.objects.get(pk=int(request.session.get('current_rest','0')))
    ro = Restaurant_Order.objects.all()
    all_orders = []
    for ri in ro:
        if ri.restaurant_id.r_id==r.r_id:
            order = ri.order_id
            cart_item = ri.cart_item_id
            cart_contains = Cart_Contains.objects.all()
            if cart_item.status!="delivered":
                for cc in cart_contains:
                    if cc.cart_item_id.cart_item_id==cart_item.cart_item_id:
                        cart = cc.cart_id
                        user_cart = User_Cart.objects.all()
                        for uc in user_cart:
                            if uc.cart_id.cart_id==cc.cart_id.cart_id:
                                cust = Customer.objects.get(pk=uc.user_id.u_id)
                                all_orders.append({'order':order,'cust':cust,'cart_item':cart_item})

    context = {
        'r':r,
        'all_orders':all_orders,
    }
    return render(request, 'polls/restaurant_orders.html',context)

def list_delivered_orders(request):
    r = Restaurant.objects.get(pk=int(request.session.get('current_rest','0')))
    ro = Restaurant_Order.objects.all()
    all_orders = []
    for ri in ro:
        if ri.restaurant_id.r_id==r.r_id:
            order = ri.order_id
            cart_item = ri.cart_item_id
            cart_contains = Cart_Contains.objects.all()
            if cart_item.status=="delivered":
                for cc in cart_contains:
                    if cc.cart_item_id.cart_item_id==cart_item.cart_item_id:
                        cart = cc.cart_id
                        user_cart = User_Cart.objects.all()
                        for uc in user_cart:
                            if uc.cart_id.cart_id==cc.cart_id.cart_id:
                                cust = Customer.objects.get(pk=uc.user_id.u_id)
                                all_orders.append({'order':order,'cust':cust,'cart_item':cart_item})

    context = {
        'r':r,
        'all_orders':all_orders,
    }
    return render(request, 'polls/restaurant_orders.html',context)

def rest_by_name(request):
    rest_list = Restaurant.objects.all().filter(r_name=request.POST['rest_city'])
    cuisine_list = Cuisine.objects.all()
    cur_user = Customer.objects.get(pk=int(request.session.get('current_user','0')))
    if cur_user.u_latest_cart_id:
        cart_items_count=0
        cart_items = Cart_Contains.objects.all()
        for lol in cart_items:
            if lol.cart_id.cart_id==cur_user.u_latest_cart_id:
                cart_items_count = cart_items_count+lol.cart_item_id.quantity
        
    else:
        cart_items_count = 0
    
    context ={
        'rest_list':rest_list,
        'cuisine_list':cuisine_list,
        'cart_items_count':cart_items_count,
    }
    return render(request, 'polls/listing.html',context)