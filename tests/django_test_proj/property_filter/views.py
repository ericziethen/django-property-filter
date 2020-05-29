
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from django_filters.views import FilterView

from property_filter.models import (
    NumberClass,
)

from . import filters

class HomePageView(TemplateView):
    template_name = 'home.html'


# Create your views here.
class NumberClassList(FilterView):
    model = NumberClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyNumberFilterSet
