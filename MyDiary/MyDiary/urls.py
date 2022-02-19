"""MyDiary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from MyDiaryapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', views.user_signup),
    path('api/login/', views.user_login),
    path('api/logout/<userid>', views.logout),
    path('api/delete/<userid>', views.user_delete),
    path('api/profile/', views.user_profile),
    path('api/create_journal/', views.create_journals),
    path('api/all_journals/<id>', views.all_journals),
    path('api/update_journals/', views.update_journals),
    path('api/journal_delete/<id>', views.journal_delete),
    path('api/create_pages/', views.create_pages),
    path('api/all_pages/<id>', views.all_pages),
    path('api/update_pages/', views.update_pages),
    path('api/page_delete/<id>', views.page_delete)
]
