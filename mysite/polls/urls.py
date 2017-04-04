from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^login_check/$', views.login_check, name='login_check'),
    url(r'^rest_by_city/(?P<city>[0-9]+)/$', views.rest_by_city, name='rest_by_city'),
    url(r'^rest_by_name/$', views.rest_by_name, name='rest_by_name'),
    url(r'^food_by_rest/(?P<rest_id>[0-9]+)/$', views.food_by_rest, name='food_by_rest'),
    url(r'^food_by_rest/(?P<rest_id>[0-9]+)/added/(?P<it_id>[0-9]+)/$', views.added, name='added'),
    url(r'^remove/(?P<cc_id>[0-9]+)/$', views.remove, name='remove'),
    url(r'^cart/$', views.cart_checkout, name='cart_checkout'),
    url(r'^confirm_cart/$', views.confirm_cart, name='confirm_cart'),
    url(r'^make_payment/$', views.make_payment, name='make_payment'),
    url(r'^track/$', views.track, name='track'),
    url(r'^cook/(?P<order>[0-9]+)/(?P<cart_item>[0-9]+)/$', views.cook, name='cook'),
    url(r'^deliver/(?P<order>[0-9]+)/(?P<cart_item>[0-9]+)/$', views.deliver, name='deliver'),
    url(r'^done/(?P<order>[0-9]+)/(?P<cart_item>[0-9]+)/$', views.done, name='done'),
    url(r'^list_delivered_orders/$', views.list_delivered_orders, name='list_delivered_orders'),
    
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
