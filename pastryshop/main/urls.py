from .import views
from django.urls import path
urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='Register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('pastry/', views.pastry, name='pastry'),
    path('about/',views.about,name='about'),
    path('shop/',views.shop,name='shop'),
    path('addtocart/',views.addtocart,name='addtocart'),
    path('removefromcart/', views.removefromcart, name='removefromcart'),
    path('cart/', views.showcart, name='showcart'),
    path('update_profile/',views.update_profile,name='update_profile'),
   path('place_order/', views.place_order, name='place_order'),
   path('payment/', views.payment, name='payment')
]

