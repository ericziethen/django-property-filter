
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from django_filters.views import FilterView

from property_filter.models import (
    AllValuesFilterModel,
    AllValuesMultipleFilterModel,
    BaseCSVFilterModel,
    BaseInFilterModel,
    BaseRangeFilterModel,
    BooleanFilterModel,
    CharFilterModel,
    ChoiceFilterModel,
    DateFilterModel,
    DateFromToRangeFilterModel,
    DateRangeFilterModel,
    DateTimeFilterModel,
    DateTimeFromToRangeFilterModel,
    DurationFilterModel,
    IsoDateTimeFilterModel,
    IsoDateTimeFromToRangeFilterModel,
    LookupChoiceFilterModel,
    ModelChoiceFilterModel,
    ModelChoiceFilterRelatedModel,
    MultiFilterTestModel,
    RelatedMultiFilterTestModel,
    MultipleChoiceFilterModel,
    NumberFilterModel,
    NumericRangeFilterModel,
    OrderingFilterModel,
    RangeFilterModel,
    TimeFilterModel,
    TimeRangeFilterModel,
    TypedChoiceFilterModel,
    TypedMultipleChoiceFilterModel,
    UUIDFilterModel,
    VolumeTestModel,
)

from . import filters

class HomePageView(TemplateView):
    template_name = 'home.html'


class AllValuesFilterView(FilterView):
    model = AllValuesFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyAllValuesFilterSet


class AllValuesMultipleFilterView(FilterView):
    model = AllValuesMultipleFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyAllValuesMultipleFilterSet


class BaseCSVFilterView(FilterView):
    model = BaseCSVFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyBaseCSVFilterSet


class BaseInFilterView(FilterView):
    model = BaseInFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyBaseInFilterSet


class BaseRangeFilterView(FilterView):
    model = BaseRangeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyBaseRangeFilterSet


class BooleanFilterView(FilterView):
    model = BooleanFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyBooleanFilterSet


class CharFilterView(FilterView):
    model = CharFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyCharFilterSet


class ChoiceFilterView(FilterView):
    model = ChoiceFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyChoiceFilterSet


class DateFilterView(FilterView):
    model = DateFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateFilterSet


class DateFromToRangeFilterView(FilterView):
    model = DateFromToRangeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateFromToRangeFilterSet


class DateRangeFilterView(FilterView):
    model = DateRangeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyDateRangeFilterSet


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


class IsoDateTimeFilterView(FilterView):
    model = IsoDateTimeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyIsoDateTimeFilterSet


class IsoDateTimeFromToRangeFilterView(FilterView):
    model = IsoDateTimeFromToRangeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyIsoDateTimeFromToRangeFilterSet


class LookupChoiceFilterView(FilterView):
    model = LookupChoiceFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyLookupChoiceFilterSet


class ModelChoiceFilterView(FilterView):
    model = ModelChoiceFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyModelChoiceFilterSet


class ModelMultipleChoiceFilterView(FilterView):
    model = ModelChoiceFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyModelMultipleChoiceFilterSet


class MultipleChoiceFilterView(FilterView):
    model = MultipleChoiceFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyMultipleChoiceFilterSet


class NumberFilterView(FilterView):
    model = NumberFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyNumberFilterSet


class NumericRangeFilterView(FilterView):
    model = NumericRangeFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyNumericRangeFilterSet


class OrderingFilterView(FilterView):
    model = OrderingFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyOrderingFilterSet


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


class TypedChoiceFilterView(FilterView):
    model = TypedChoiceFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyTypedChoiceFilterSet


class TypedMultipleChoiceFilterView(FilterView):
    model = TypedMultipleChoiceFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyTypedMultipleChoiceFilterSet


class UUIDFilterView(FilterView):
    model = UUIDFilterModel
    template_name = 'generic_filter.html'
    filterset_class = filters.PropertyUUIDFilterSet


class VolumeTestView(FilterView):
    model = VolumeTestModel
    template_name = 'generic_filter_filter_first.html'
    filterset_class = filters.VolumeTestFilterSet


class MultiFilterTestView(FilterView):
    model = MultiFilterTestModel
    template_name = 'generic_filter_filter_first.html'
    filterset_class = filters.MultiFilterTestFilterSet


class RelatedMultiFilterTestView(FilterView):
    model = RelatedMultiFilterTestModel
    template_name = 'generic_filter_filter_first.html'
    filterset_class = filters.RelatedMultiFilterTestFilterSet


class MiscBooleanChoiceFiltersView(FilterView):
    model = BooleanFilterModel
    template_name = 'generic_filter_filter_first.html'
    filterset_class = filters.MiscBooleanChoiceFiltersFilterSet
