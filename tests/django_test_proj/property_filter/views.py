
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from django_filters.views import FilterView

from property_filter.models import (
    BooleanClass,
    DateClass,
    DateTimeClass,
    DurationClass,
    NumberClass,
    TextClass,
    TimeClass,
)

from . import filters

class HomePageView(TemplateView):
    template_name = 'home.html'


class BooleanClassList(FilterView):
    model = BooleanClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyBooleanFilterSet


class CharClassList(FilterView):
    model = TextClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyCharFilterSet


class DateClassList(FilterView):
    model = DateClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateFilterSet


class DateFromToRangeList(FilterView):
    model = DateClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateFromToRangeFilterSet


class DateTimeClassList(FilterView):
    model = DateTimeClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateTimeFilterSet


class DurationClassList(FilterView):
    model = DurationClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDurationFilterSet


# Create your views here.
class NumberClassList(FilterView):
    model = NumberClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyNumberFilterSet


class NumberClassRangeList(FilterView):
    model = NumberClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyRangeFilterSet


class TimeClassList(FilterView):
    model = TimeClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyTimeFilterSet


class TimeClassRangeList(FilterView):
    model = TimeClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyTimeRangeFilterSet
