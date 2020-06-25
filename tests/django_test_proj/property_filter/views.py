
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from django_filters.views import FilterView

from property_filter.models import (
    BooleanFilterModel,
    CharFilterModel,
    DateFilterModel,
    DateFromToRangeFilterModel,
    DateTimeFilterModel,
    DateTimeFromToRangeFilterModel,
    DurationFilterModel,
    NumberFilterModel,
    RangeFilterModel,
    TimeFilterModel,
    TimeRangeFilterModel,
)

from . import filters

class HomePageView(TemplateView):
    template_name = 'home.html'


class BooleanFilterView(FilterView):
    model = BooleanFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyBooleanFilterSet


class CharFilterView(FilterView):
    model = CharFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyCharFilterSet


class DateFilterView(FilterView):
    model = DateFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateFilterSet


class DateFromToRangeFilterView(FilterView):
    model = DateFromToRangeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateFromToRangeFilterSet


class DateTimeFilterView(FilterView):
    model = DateTimeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateTimeFilterSet


class DateTimeFromToRangeFilterView(FilterView):
    model = DateTimeFromToRangeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateTimeFromToRangeFilterSet


class DurationFilterView(FilterView):
    model = DurationFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDurationFilterSet


# Create your views here.
class NumberFilterView(FilterView):
    model = NumberFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyNumberFilterSet


class RangeFilterView(FilterView):
    model = RangeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyRangeFilterSet


class TimeFilterView(FilterView):
    model = TimeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyTimeFilterSet


class TimeRangeFilterView(FilterView):
    model = TimeRangeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyTimeRangeFilterSet
