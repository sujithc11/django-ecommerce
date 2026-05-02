from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('login/', views.login_user, name='login'),   # ✅ important
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),
    path('update/<int:id>/', views.update_product, name='update_product'),
    path('buy/<int:id>/', views.buy_now, name='buy_now'),
]