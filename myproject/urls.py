"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.display_page, name='display_page'),
    path('start/', views.start, name='start'),
    
    path('home/', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('graph/', views.product_graph, name='product_graph'),
    path('shop/', views.shop, name='shop'),
     
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('graph-data/', views.graph_data, name='graph-data'),
    path('graph-data/', views.graph_data, name='graph_data'),
    path('analysis/', views.analysis, name='analysis'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'), 
    path('logout/', views.user_logout, name='logout'),
]


 
