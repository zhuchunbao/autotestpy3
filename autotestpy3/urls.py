"""autotestpy3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from apitest import views
from product import proviews
from set import setviews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.test),
    path('login/', views.login),
    path(r'home/', views.home),
    path(r'logout/', views.logout),
    path('product_manage/', proviews.product_manage),
    path('apitest_manage/', views.apitest_manage),
    path('apistep_manage/', views.apistep_manage),
    path('apis_manage/', views.apis_manage),
    path('set_manage/', setviews.set_manage),
    path('set_user/', setviews.set_user),
    path('test_report/', views.test_report),
    path('left/', views.left),
    path ('apisearch/', views.apisearch),
    path ('apissearch/', views.apissearch),
    path ('setsearch/', setviews.setsearch),
    path ('productsearch/', proviews.productsearch),
]
