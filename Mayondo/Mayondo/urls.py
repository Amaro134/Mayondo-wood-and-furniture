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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Wood import views   # import views, not models

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication routes
    path('', include('authentication.urls')),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Stock management routes
    path('inventory/', include([
        path('add/', views.addStock, name='addStock'),
        path('list/', views.stock_list, name='stock_list'),
        path('<int:id>/edit/', views.stockedit, name='stockedit'),
        path('<int:id>/view/', views.stockview, name='stockview'),
        path('<int:id>/delete/', views.stockdelete, name='stockdelete'),
    ])),
    
    # Sales management routes  
    path('sales/', include([
        path('add/', views.add_sales, name="add_sales"),
        path('list/', views.sales_list, name="sales_list"),
        path('<int:id>/edit/', views.salesedit, name='salesedit'),
        path('<int:id>/delete/', views.salesdelete, name='sales_delete'),
        path('<int:id>/view/', views.salesview, name='salesview'),
        path('<int:sale_id>/receipt/', views.salesreceipt, name='salesreceipt'),
    ])),
    
    # User management routes
    path('users/', include([
        path('list/', views.user_list, name='user_list'),
        path('add/', views.adduser, name='add_user'),
        path('<int:id>/edit/', views.user_edit, name='user_edit'),
        path('<int:id>/delete/', views.user_delete, name='user_delete'),
        path('<int:id>/view/', views.user_view, name='user_view'),
    ])),
    
    # Reports routes
    path('reports/', include([
        path('', views.report_dashboard, name='report_dashboard'),
        path('sales/', views.sales_report, name='sales_report'),
        path('stock/', views.stock_report, name='stock_report'),
        path('summary/', views.summary_report, name='summary_report'),
    ])),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

