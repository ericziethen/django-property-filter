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
    path('boolean_filter/', views.BooleanFilterView.as_view(), name='boolean_filter'),
    path('char_filter/', views.CharFilterView.as_view(), name='char_filter'),
    path('date_filter/', views.DateFilterView.as_view(), name='date_filter'),
    path('date_from_to_range_filter/', views.DateFromToRangeFilterView.as_view(), name='date_from_to_range_filter'),
    path('date_time_filter/', views.DateTimeFilterView.as_view(), name='date_time_filter'),
    path('duration_filter/', views.DurationFilterView.as_view(), name='duration_filter'),



    path('numberclasses/', views.NumberClassList.as_view(), name='numberclass_list'),
    path('numberclassesrange/', views.NumberClassRangeList.as_view(), name='numberclassrange_list'),
    path('timeclasses/', views.TimeClassList.as_view(), name='timeclass_list'),
    path('timeclassesrange/', views.TimeClassRangeList.as_view(), name='timeclassrange_list'),
]
