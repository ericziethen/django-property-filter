"""django_test_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from property_filter import models, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('booleanclasses/', views.BooleanClassList.as_view(), name='booleanclass_list'),
    path('charclasses/', views.CharClassList.as_view(), name='charclass_list'),
    path('dateclasses/', views.DateClassList.as_view(), name='dateclass_list'),
    path('date_from_to_range_filter/', views.DateFromToRangeView.as_view(), name='date_from_to_range_filter'),
    path('datetimeclasses/', views.DateTimeClassList.as_view(), name='datetimeclass_list'),
    path('durationclasses/', views.DurationClassList.as_view(), name='durationclass_list'),
    path('numberclasses/', views.NumberClassList.as_view(), name='numberclass_list'),
    path('numberclassesrange/', views.NumberClassRangeList.as_view(), name='numberclassrange_list'),
    path('timeclasses/', views.TimeClassList.as_view(), name='timeclass_list'),
    path('timeclassesrange/', views.TimeClassRangeList.as_view(), name='timeclassrange_list'),
]
