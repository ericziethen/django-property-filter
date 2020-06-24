
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
    DateFromToRangeFilterModel,
)

from . import filters

class HomePageView(TemplateView):
    template_name = 'home.html'


class BooleanFilterView(FilterView):
    model = BooleanClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyBooleanFilterSet


class CharFilterView(FilterView):
    model = TextClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyCharFilterSet


class DateFilterView(FilterView):
    model = DateClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateFilterSet


class DateFromToRangeFilterView(FilterView):
    model = DateFromToRangeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateFromToRangeFilterSet


class DateTimeFilterView(FilterView):
    model = DateTimeClass
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateTimeFilterSet


class DurationFilterView(FilterView):
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
