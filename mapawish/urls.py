"""
URL configuration for mapawish project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from mnotes.views import logout_view

from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView


urlpatterns = [
    path("", include("mnotes.urls")),
    path("accounts/logout/", logout_view, name="logout"),
    path("accounts/", include("allauth.urls")),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("admin/", admin.site.urls),
]
