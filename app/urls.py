"""Covid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from app import views

urlpatterns = [
    path("",views.welcome,name='app'),
    path("home",views.home,name='home'),
    path("update",views.update,name='update'),
    path("riskpredictor",views.riskpredictor,name='riskpredictor'),
    path("about",views.about,name='about'),
    path("loading",views.loading,name='loading'),
    path("results",views.results,name='results'),
    path("contact",views.contact,name='contact'),
    path("vaccine",views.vaccine,name='vaccine'),
    path("dashboard",views.dashboard,name='dashboard'),
    path("email",views.email,name='email')
]
