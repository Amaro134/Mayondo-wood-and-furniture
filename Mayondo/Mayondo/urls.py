"""
URL configuration for Mayondo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Wood import views   # import views, not models

urlpatterns = [
    path('admin/', admin.site.urls),
    
     # Landing page
    path('', views.landingPage, name="landingPage"),
    path('login/', views.loginPage, name='login'),  # login page
    # Stock routes
    path('addStock/', views.addStock, name='addStock'),  # shows stock form & handles submit
    path('stock/', views.stock_list, name='stock_list'),
   path('stockedit/<int:id>/', views.stockedit, name='stockedit'),# lists all
    path('stockview/<int:id>/', views.stockview, name='stockview'),
    path('stockdelete/<int:id>/', views.stockdelete, name='stockdelete'),  # delete stock
    path('stockupdate/<int:id>/', views.stockupdate, name='stockupdate'),
    # Sales routes
    path("add_sales/", views.add_sales, name="add_sales"),   # shows sales form & handles submit
    path("sales_list/", views.sales_list, name="sales_list"),# view one stock item
    path('salesedit/<int:id>/', views.salesedit, name='salesedit'),  # edit sales
    path('salesdelete/<int:id>/', views.salesdelete, name='sales_delete'),
    path('salesview/<int:id>/', views.salesview, name='salesview'), 
    # update sales
    # path('report/', views.report_view, name='report'),
    #dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # User routes
    path('user_list/', views.user_list, name='user_list'),  # lists all users
    path('add_user/', views.adduser, name='add_user'),  # shows user
    path('useredit/<int:id>/', views.user_edit, name='user_edit'),  # edit user
    path('user_delete/<int:id>/', views.user_delete, name='user_delete'),  # delete user
    path('user_view/<int:id>/', views.user_view, name='user_view'),  # view user details
    path('logout/', views.logout, name='logout'),  # logout user
]
