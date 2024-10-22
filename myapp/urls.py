from django.urls import path
from . import views
from .views import logout_view  
urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('signup/', views.user_signup, name='signup'),
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('get_stock_data/', views.get_stock_data, name='get_stock_data'),
    path('stock_detail/', views.stock_detail, name='stock_detail'),
    path('save_stock/', views.home, name='save_stock'),  
    path('saved_stocks/', views.saved_stocks, name='saved_stocks'),
    path('delete_stock/<int:stock_id>/', views.delete_stock, name='delete_stock'),

    path('get_nifty_data/', views.get_nifty_data, name='get_nifty_data'),
    path('get_sensex_data/', views.get_sensex_data, name='get_sensex_data'),
]
