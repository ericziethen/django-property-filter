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
    path('all_values_filter/', views.AllValuesFilterView.as_view(), name='all_values_filter'),
    path('all_values_multiple_filter/', views.AllValuesMultipleFilterView.as_view(), name='all_values_multiple_filter'),
    path('base_csv_filter/', views.BaseCSVFilterView.as_view(), name='base_csv_filter'),
    path('base_in_filter/', views.BaseInFilterView.as_view(), name='base_in_filter'),
    path('base_range_filter/', views.BaseRangeFilterView.as_view(), name='base_range_filter'),
    path('boolean_filter/', views.BooleanFilterView.as_view(), name='boolean_filter'),
    path('char_filter/', views.CharFilterView.as_view(), name='char_filter'),
    path('choice_filter/', views.ChoiceFilterView.as_view(), name='choice_filter'),
    path('date_filter/', views.DateFilterView.as_view(), name='date_filter'),
    path('date_from_to_range_filter/', views.DateFromToRangeFilterView.as_view(), name='date_from_to_range_filter'),
    path('date_range_filter/', views.DateRangeFilterView.as_view(), name='date_range_filter'),
    path('date_time_filter/', views.DateTimeFilterView.as_view(), name='date_time_filter'),
    path('date_time_from_to_range_filter/', views.DateTimeFromToRangeFilterView.as_view(), name='date_time_from_to_range_filter'),
    path('duration_filter/', views.DurationFilterView.as_view(), name='duration_filter'),
    path('iso_date_time_filter/', views.IsoDateTimeFilterView.as_view(), name='iso_date_time_filter'),
    path('iso_date_time_from_to_range_filter/', views.IsoDateTimeFromToRangeFilterView.as_view(), name='iso_date_time_from_to_range_filter'),
    path('lookup_choice_filter/', views.LookupChoiceFilterView.as_view(), name='lookup_choice_filter'),    
    path('model_choice_filter/', views.ModelChoiceFilterView.as_view(), name='model_choice_filter'),
    path('model_multiple_choice_filter/', views.ModelMultipleChoiceFilterView.as_view(), name='model_multiple_choice_filter'),
    path('multi_filter_test/', views.MultiFilterTestView.as_view(), name='multi_filter_test'),
    path('multiple_choice_filter/', views.MultipleChoiceFilterView.as_view(), name='multiple_choice_filter'),
    path('number_filter/', views.NumberFilterView.as_view(), name='number_filter'),
    path('numeric_range_filter/', views.NumericRangeFilterView.as_view(), name='numeric_range_filter'),
    path('ordering_filter/', views.OrderingFilterView.as_view(), name='ordering_filter'),
    path('range_filter/', views.RangeFilterView.as_view(), name='range_filter'),
    path('time_filter/', views.TimeFilterView.as_view(), name='time_filter'),
    path('time_range_filter/', views.TimeRangeFilterView.as_view(), name='time_range_filter'),
    path('typed_choice_filter/', views.TypedChoiceFilterView.as_view(), name='typed_choice_filter'),
    path('typed_mutiple_choice_filter/', views.TypedMultipleChoiceFilterView.as_view(), name='typed_mutiple_choice_filter'),
    path('uuid_filter/', views.UUIDFilterView.as_view(), name='uuid_filter'),
    path('volume_test/', views.VolumeTestView.as_view(), name='volume_test'),
    path('boolean_choice_test/', views.MiscBooleanChoiceFiltersView.as_view(), name='boolean_choice_test'),
]
