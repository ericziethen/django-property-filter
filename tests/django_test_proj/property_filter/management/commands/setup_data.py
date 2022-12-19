
import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..', '..')))

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.utils import timezone
from django.utils.timezone import make_aware

from tests.common import db_is_postgresql

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
)

try:
    from psycopg2.extras import NumericRange
except ImportError:
    pass


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(F'VENDOR: "{connection.vendor}"')

        with transaction.atomic():
            # Clear the Data
            call_command('flush', verbosity=0, interactive=False)

            # Add the Data
            print('>> Setup Generic Data')
            self.setup_all_values_filter_model()
            self.setup_all_values_multiple_filter_model()
            self.setup_base_csv_filter_model()
            self.setup_base_in_filter_model()
            self.setup_base_range_filter_model()
            self.setup_boolean_filter_model()
            self.setup_char_filter_model()
            self.setup_choice_filter_model()
            self.setup_date_filter_model()
            self.setup_date_from_to_range_filter_model()
            self.setup_date_range_filter_model()
            self.setup_date_time_filter_model()
            self.setup_date_time_from_to_range_filter_model()
            self.setup_duration_filter_model()
            self.setup_iso_date_time_filter_model()
            self.setup_iso_date_time_from_to_range_filter_model()
            self.setup_lookup_choice_filter_model()
            self.setup_model_choice_filter_model()
            self.setup_multi_filter_test_model()
            self.setup_multiple_choice_filter_model()
            self.setup_number_filter_model()
            self.setup_ordering_filter_model()
            self.setup_range_filter_model()
            self.setup_time_filter_model()
            self.setup_time_range_filter_model()
            self.setup_typed_choice_filter_model()
            self.setup_typed_multiple_choice_filter_model()
            self.setup_uuid_filter_model()

            if db_is_postgresql():
                print('>> Setup Postgresql only Data')
                self.setup_numeric_range_filter_model()

        print('>> Setup Finished')

    def setup_all_values_filter_model(self):
        print('Setup AllValuesFilterModel')

        AllValuesFilterModel.objects.create(id=-1, number=-1)
        AllValuesFilterModel.objects.create(id=0, number=0)
        AllValuesFilterModel.objects.create(id=1, number=1)
        AllValuesFilterModel.objects.create(id=2, number=2)
        AllValuesFilterModel.objects.create(id=3, number=2)
        AllValuesFilterModel.objects.create(id=4, number=2)
        AllValuesFilterModel.objects.create(id=5, number=3)
        AllValuesFilterModel.objects.create(id=6, number=4)
        AllValuesFilterModel.objects.create(id=7, number=10)
        AllValuesFilterModel.objects.create(id=8, number=20)
        AllValuesFilterModel.objects.create(id=9)

    def setup_all_values_multiple_filter_model(self):
        print('Setup AllValuesMultipleFilterModel')

        AllValuesMultipleFilterModel.objects.create(id=-1, number=-1)
        AllValuesMultipleFilterModel.objects.create(id=0, number=0)
        AllValuesMultipleFilterModel.objects.create(id=1, number=1)
        AllValuesMultipleFilterModel.objects.create(id=2, number=2)
        AllValuesMultipleFilterModel.objects.create(id=3, number=2)
        AllValuesMultipleFilterModel.objects.create(id=4, number=2)
        AllValuesMultipleFilterModel.objects.create(id=5, number=3)
        AllValuesMultipleFilterModel.objects.create(id=6, number=4)
        AllValuesMultipleFilterModel.objects.create(id=7, number=10)
        AllValuesMultipleFilterModel.objects.create(id=8, number=20)
        AllValuesMultipleFilterModel.objects.create(id=9)

    def setup_base_csv_filter_model(self):
        print('Setup BaseCSVFilterModel')

        BaseCSVFilterModel.objects.create(id=1, number=1, text='Another')
        BaseCSVFilterModel.objects.create(id=2, number=2, text='Best')
        BaseCSVFilterModel.objects.create(id=3, number=3, text='Clear')
        BaseCSVFilterModel.objects.create(id=4, number=3, text='clear')
        BaseCSVFilterModel.objects.create(id=5, number=4, text='date')
        BaseCSVFilterModel.objects.create(id=6, number=10, text='Hello')
        BaseCSVFilterModel.objects.create(id=7, number=20, text='zebra')

    def setup_base_in_filter_model(self):
        print('Setup BaseInFilterModel')

        BaseInFilterModel.objects.create(id=1, number=-1.25)
        BaseInFilterModel.objects.create(id=2, number=0.0)
        BaseInFilterModel.objects.create(id=3, number=0)
        BaseInFilterModel.objects.create(id=4, number=1.0)
        BaseInFilterModel.objects.create(id=5, number=1.1)
        BaseInFilterModel.objects.create(id=6, number=3.5)
        BaseInFilterModel.objects.create(id=7, number=20.99)

    def setup_base_range_filter_model(self):
        print('Setup BaseRangeFilterModel')

        BaseRangeFilterModel.objects.create(id=1, date=datetime.date(2018, 2, 1))
        BaseRangeFilterModel.objects.create(id=2, date=datetime.date(2019, 3, 2))
        BaseRangeFilterModel.objects.create(id=3, date=datetime.date(2019, 3, 2))
        BaseRangeFilterModel.objects.create(id=4, date=datetime.date(2019, 3, 4))
        BaseRangeFilterModel.objects.create(id=5, date=datetime.date(2020, 2, 5))
        BaseRangeFilterModel.objects.create(id=6, date=datetime.date(2020, 2, 6))
        BaseRangeFilterModel.objects.create(id=7, date=datetime.date(2020, 2, 6))
        BaseRangeFilterModel.objects.create(id=8, date=datetime.date(2020, 2, 6))
        BaseRangeFilterModel.objects.create(id=9, date=datetime.date(2020, 2, 9))

    def setup_boolean_filter_model(self):
        print('Setup BooleanFilterModel')

        BooleanFilterModel.objects.create(id=1, is_true=True)
        BooleanFilterModel.objects.create(id=2, is_true=False)
        BooleanFilterModel.objects.create(id=3, )
        BooleanFilterModel.objects.create(id=4, is_true=True)
        BooleanFilterModel.objects.create(id=5, is_true=False)
        BooleanFilterModel.objects.create(id=6, )

    def setup_char_filter_model(self):
        print('Setup CharFilterModel')

        CharFilterModel.objects.create(id=-1, name='Aa')
        CharFilterModel.objects.create(id=0, name='BB')
        CharFilterModel.objects.create(id=1, name='bb')
        CharFilterModel.objects.create(id=2, name='C')
        CharFilterModel.objects.create(id=3, name='c')
        CharFilterModel.objects.create(id=4)

    def setup_choice_filter_model(self):
        print('Setup ChoiceFilterModel')

        ChoiceFilterModel.objects.create(id=-1, number=-1)
        ChoiceFilterModel.objects.create(id=0, number=0)
        ChoiceFilterModel.objects.create(id=1, number=1)
        ChoiceFilterModel.objects.create(id=2, number=2)
        ChoiceFilterModel.objects.create(id=3, number=2)
        ChoiceFilterModel.objects.create(id=4, number=2)
        ChoiceFilterModel.objects.create(id=5, number=3)
        ChoiceFilterModel.objects.create(id=6, number=4)
        ChoiceFilterModel.objects.create(id=7, number=10)
        ChoiceFilterModel.objects.create(id=8, number=20)
        ChoiceFilterModel.objects.create(id=9)

    def setup_date_filter_model(self):
        print('Setup DateFilterModel')

        DateFilterModel.objects.create(id=1, date=datetime.date(2018, 2, 1))
        DateFilterModel.objects.create(id=2, date=datetime.date(2019, 3, 2))
        DateFilterModel.objects.create(id=3, date=datetime.date(2019, 3, 2))
        DateFilterModel.objects.create(id=4, date=datetime.date(2019, 3, 4))
        DateFilterModel.objects.create(id=5, date=datetime.date(2020, 2, 5))
        DateFilterModel.objects.create(id=6, date=datetime.date(2020, 2, 6))
        DateFilterModel.objects.create(id=7, date=datetime.date(2020, 2, 6))
        DateFilterModel.objects.create(id=8, date=datetime.date(2020, 2, 6))
        DateFilterModel.objects.create(id=9, date=datetime.date(2020, 2, 9))

    def setup_date_from_to_range_filter_model(self):
        print('Setup DateFromToRangeFilterModel')

        tz = timezone.get_default_timezone()

        DateFromToRangeFilterModel.objects.create(
            id=-1,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2018, 2, 1, 13, 30, tzinfo=tz))
        DateFromToRangeFilterModel.objects.create(
            id=0,
            date=datetime.date(2019, 3, 2),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        DateFromToRangeFilterModel.objects.create(
            id=1,
            date=datetime.date(2019, 3, 2),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        DateFromToRangeFilterModel.objects.create(
            id=2,
            date=datetime.date(2019, 3, 4),
            date_time=datetime.datetime(2019, 3, 4, 12, 0, tzinfo=tz))
        DateFromToRangeFilterModel.objects.create(
            id=3,
            date=datetime.date(2020, 2, 5),
            date_time=datetime.datetime(2020, 2, 5, 12, 0, 0, tzinfo=tz))
        DateFromToRangeFilterModel.objects.create(
            id=4,
            date=datetime.date(2020, 2, 6),
            date_time=datetime.datetime(2020, 2, 6, 13, 30, tzinfo=tz))

    def setup_date_range_filter_model(self):
        print('Setup DateRangeFilterModel')

        today_datetime = timezone.now()

        DateRangeFilterModel.objects.create(
            id=-1,
            date=today_datetime.date(),
            date_time=today_datetime)

        DateRangeFilterModel.objects.create(
            id=0,
            date=today_datetime.date() - datetime.timedelta(days=1),
            date_time=today_datetime - datetime.timedelta(days=1))

        DateRangeFilterModel.objects.create(
            id=1,
            date=today_datetime.date() - datetime.timedelta(days=6),
            date_time=today_datetime - datetime.timedelta(days=6))

        DateRangeFilterModel.objects.create(
            id=2,
            date=today_datetime.date() - datetime.timedelta(days=7),
            date_time=today_datetime - datetime.timedelta(days=7))

        DateRangeFilterModel.objects.create(
            id=3,
            date=today_datetime.date() - datetime.timedelta(days=15),
            date_time=today_datetime - datetime.timedelta(days=15))

        DateRangeFilterModel.objects.create(
            id=4,
            date=today_datetime.date() + datetime.timedelta(days=15),
            date_time=today_datetime + datetime.timedelta(days=15))

        DateRangeFilterModel.objects.create(
            id=5,
            date=today_datetime.date() + datetime.timedelta(days=400),
            date_time=today_datetime + datetime.timedelta(days=400))

        DateRangeFilterModel.objects.create(
            id=6,
            date=today_datetime.date() - datetime.timedelta(days=800),
            date_time=today_datetime - datetime.timedelta(days=800))

    def setup_date_time_filter_model(self):
        print('Setup DateTimeFilterModel')

        DateTimeFilterModel.objects.create(id=1, date_time=make_aware(datetime.datetime(2020, 1, 1, 13, 30)))
        DateTimeFilterModel.objects.create(id=2, date_time=make_aware(datetime.datetime(2020, 1, 1, 13, 40)))
        DateTimeFilterModel.objects.create(id=3, date_time=make_aware(datetime.datetime(2020, 2, 2, 12)))
        DateTimeFilterModel.objects.create(id=4, date_time=make_aware(datetime.datetime(2020, 2, 2, 12, 0)))
        DateTimeFilterModel.objects.create(id=5, date_time=make_aware(datetime.datetime(2020, 2, 2, 12, 0, 0)))
        DateTimeFilterModel.objects.create(id=6, date_time=make_aware(datetime.datetime(2021, 1, 1, 13, 30)))
        DateTimeFilterModel.objects.create(id=7, date_time=make_aware(datetime.datetime(2021, 1, 1, 13, 30)))
        DateTimeFilterModel.objects.create(id=8, date_time=make_aware(datetime.datetime(2022, 1, 1, 13, 30)))

    def setup_date_time_from_to_range_filter_model(self):
        print('Setup DateTimeFromToRangeFilterModel')

        DateTimeFromToRangeFilterModel.objects.create(id=1, date_time=make_aware(datetime.datetime(2020, 1, 1, 13, 30)))
        DateTimeFromToRangeFilterModel.objects.create(id=2, date_time=make_aware(datetime.datetime(2020, 1, 1, 13, 40)))
        DateTimeFromToRangeFilterModel.objects.create(id=3, date_time=make_aware(datetime.datetime(2020, 2, 2, 12)))
        DateTimeFromToRangeFilterModel.objects.create(id=4, date_time=make_aware(datetime.datetime(2020, 2, 2, 12, 0)))
        DateTimeFromToRangeFilterModel.objects.create(id=5, date_time=make_aware(datetime.datetime(2020, 2, 2, 12, 0, 0)))
        DateTimeFromToRangeFilterModel.objects.create(id=6, date_time=make_aware(datetime.datetime(2021, 1, 1, 13, 30)))
        DateTimeFromToRangeFilterModel.objects.create(id=7, date_time=make_aware(datetime.datetime(2021, 1, 1, 13, 30)))
        DateTimeFromToRangeFilterModel.objects.create(id=8, date_time=make_aware(datetime.datetime(2022, 1, 1, 13, 30)))

    def setup_duration_filter_model(self):
        print('Setup DurationFilterModel')

        DurationFilterModel.objects.create(id=1, duration=datetime.timedelta(hours=5))
        DurationFilterModel.objects.create(id=2, duration=datetime.timedelta(hours=5))
        DurationFilterModel.objects.create(id=3, duration=datetime.timedelta(days=1, hours=10))
        DurationFilterModel.objects.create(id=4, duration=datetime.timedelta(days=2, hours=10))
        DurationFilterModel.objects.create(id=5, duration=datetime.timedelta(days=2, hours=10))
        DurationFilterModel.objects.create(id=6, duration=datetime.timedelta(days=15))
        DurationFilterModel.objects.create(id=7, duration=datetime.timedelta(days=15))
        DurationFilterModel.objects.create(id=8, duration=datetime.timedelta(days=30))
        DurationFilterModel.objects.create(id=9, duration=datetime.timedelta(days=200))

    def setup_iso_date_time_filter_model(self):
        print('Setup IsoDateTimeFilterModel')

        IsoDateTimeFilterModel.objects.create(id=1, date_time='2020-01-03T12:00:00+12:00')
        IsoDateTimeFilterModel.objects.create(id=2, date_time='2020-01-03T12:00:00+11:00')
        IsoDateTimeFilterModel.objects.create(id=3, date_time='2020-01-03T12:00:00+10:00')
        IsoDateTimeFilterModel.objects.create(id=4, date_time='2020-12-03T12:00:00+10:00')
        IsoDateTimeFilterModel.objects.create(id=5, date_time='2020-12-03T12:00:00+10:00')
        IsoDateTimeFilterModel.objects.create(id=6, date_time='2021-12-03T12:00:00+10:00')

    def setup_iso_date_time_from_to_range_filter_model(self):
        print('Setup IsoDateTimeFromToRangeFilterModel')

        IsoDateTimeFromToRangeFilterModel.objects.create(id=1, date_time='2020-01-03T12:00:00+12:00')
        IsoDateTimeFromToRangeFilterModel.objects.create(id=2, date_time='2020-01-03T12:00:00+11:00')
        IsoDateTimeFromToRangeFilterModel.objects.create(id=3, date_time='2020-01-03T12:00:00+10:00')
        IsoDateTimeFromToRangeFilterModel.objects.create(id=4, date_time='2020-12-03T12:00:00+10:00')
        IsoDateTimeFromToRangeFilterModel.objects.create(id=5, date_time='2020-12-03T12:00:00+10:00')
        IsoDateTimeFromToRangeFilterModel.objects.create(id=6, date_time='2021-12-03T12:00:00+10:00')

    def setup_lookup_choice_filter_model(self):
        print('Setup LookupChoiceFilterModel')

        for num in range(21):
            LookupChoiceFilterModel.objects.create(number=num)

    def setup_model_choice_filter_model(self):
        print('Setup ModelChoiceFilterModel')

        related_a = ModelChoiceFilterRelatedModel.objects.create(id=1, text='AAA')
        related_b = ModelChoiceFilterRelatedModel.objects.create(id=2, text='BBB')
        related_c = ModelChoiceFilterRelatedModel.objects.create(id=3, text='CCC')
        related_d = ModelChoiceFilterRelatedModel.objects.create(id=4, text='DDD')

        ModelChoiceFilterModel.objects.create(id=1, related=related_a)
        ModelChoiceFilterModel.objects.create(id=2, related=related_a)
        ModelChoiceFilterModel.objects.create(id=3, related=related_a)
        ModelChoiceFilterModel.objects.create(id=4, related=related_c)
        ModelChoiceFilterModel.objects.create(id=5, related=related_c)
        ModelChoiceFilterModel.objects.create(id=6, related=related_d)

    def setup_multi_filter_test_model(self):
        print('Setup MultiFilterTestModel')

        tz = timezone.get_default_timezone()

        MultiFilterTestModel.objects.create(
            id=1, number=5, text='Five', is_true=True,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=2, number=999, text='Five', is_true=True,  # Different number
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=3, number=5, text='One Million', is_true=True,  # Different text
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=4, number=5, text='Five', is_true=False,  # Different is_true
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=5, number=5, text='Five', is_true=True,
            date=datetime.date(2050, 2, 1),  # Different date
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        MultiFilterTestModel.objects.create(
            id=6, number=5, text='Five', is_true=True,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2066, 3, 2, 12, tzinfo=tz))  # Different DateTime

    def setup_multiple_choice_filter_model(self):
        print('Setup MultipleChoiceFilterModel')

        MultipleChoiceFilterModel.objects.create(id=-1, number=-1)
        MultipleChoiceFilterModel.objects.create(id=0, number=0)
        MultipleChoiceFilterModel.objects.create(id=1, number=1)
        MultipleChoiceFilterModel.objects.create(id=2, number=2)
        MultipleChoiceFilterModel.objects.create(id=3, number=2)
        MultipleChoiceFilterModel.objects.create(id=4, number=2)
        MultipleChoiceFilterModel.objects.create(id=5, number=3)
        MultipleChoiceFilterModel.objects.create(id=6, number=4)
        MultipleChoiceFilterModel.objects.create(id=7, number=10)
        MultipleChoiceFilterModel.objects.create(id=8, number=20)
        MultipleChoiceFilterModel.objects.create(id=9)

    def setup_number_filter_model(self):
        print('Setup NumberFilterModel')

        for num in range(21):
            NumberFilterModel.objects.create(number=num)

    def setup_numeric_range_filter_model(self):
        print('Setup NumericRangeFilterModel')

        NumericRangeFilterModel.objects.create(id=-1,
            postgres_int_range=NumericRange(5, 10), postgres_decimal_range=NumericRange(5.0, 10.0))
        NumericRangeFilterModel.objects.create(id=0,
            postgres_int_range=NumericRange(5, 10), postgres_decimal_range=NumericRange(5.0, 10.0))
        NumericRangeFilterModel.objects.create(id=1,
            postgres_int_range=NumericRange(5, None), postgres_decimal_range=NumericRange(5.0, None))
        NumericRangeFilterModel.objects.create(id=2,
            postgres_int_range=NumericRange(None, 10), postgres_decimal_range=NumericRange(None, 10.0))
        NumericRangeFilterModel.objects.create(id=3,
            postgres_int_range=NumericRange(1, 10), postgres_decimal_range=NumericRange(1.0, 10.0))
        NumericRangeFilterModel.objects.create(id=4,
            postgres_int_range=NumericRange(5, 20), postgres_decimal_range=NumericRange(5.0, 20.0))
        NumericRangeFilterModel.objects.create(id=5,
            postgres_int_range=NumericRange(1, 20), postgres_decimal_range=NumericRange(1.0, 10.0))
        NumericRangeFilterModel.objects.create(id=6,
            postgres_int_range=NumericRange(1, 20), postgres_decimal_range=NumericRange(1.0, 10.0))
        NumericRangeFilterModel.objects.create(id=7,
            postgres_int_range=None)

    def setup_ordering_filter_model(self):
        print('Setup OrderingFilterModel')

        OrderingFilterModel.objects.create(id=-1, first_name='Bart', last_name='Simpson', username='El Barto', age=10)
        OrderingFilterModel.objects.create(id=0, first_name='Walter', last_name='White', username='Heisenberg', age=55)
        OrderingFilterModel.objects.create(id=1, first_name='Eric', last_name='Cartman', username='KylesMom', age=8)
        OrderingFilterModel.objects.create(id=2, first_name='Sonic', last_name='the Hedgehog', username='The Flash', age=16)
        OrderingFilterModel.objects.create(id=3, first_name='Lester', last_name='Nygaard', username='Innocent', age=45)
        OrderingFilterModel.objects.create(id=4, first_name='Lionel', last_name='Messi', username='Bola', age=35)
        OrderingFilterModel.objects.create(id=5, first_name='Misato', last_name='Katsuragi', username='Shinji', age=28)

    def setup_range_filter_model(self):
        print('Setup RangeFilterModel')

        for num in range(21):
            RangeFilterModel.objects.create(number=num)

    def setup_time_filter_model(self):
        print('Setup TimeFilterModel')

        TimeFilterModel.objects.create(id=1, time=datetime.time(7, 30, 15))
        TimeFilterModel.objects.create(id=2, time=datetime.time(7, 30, 15))
        TimeFilterModel.objects.create(id=3, time=datetime.time(8, 0, 0))
        TimeFilterModel.objects.create(id=4, time=datetime.time(8, 0, 0))
        TimeFilterModel.objects.create(id=5, time=datetime.time(8, 0, 0))
        TimeFilterModel.objects.create(id=6, time=datetime.time(15, 15, 15))
        TimeFilterModel.objects.create(id=7, time=datetime.time(18, 30))

    def setup_time_range_filter_model(self):
        print('Setup TimeRangeFilterModel')

        TimeRangeFilterModel.objects.create(id=1, time=datetime.time(7, 30, 15))
        TimeRangeFilterModel.objects.create(id=2, time=datetime.time(7, 30, 15))
        TimeRangeFilterModel.objects.create(id=3, time=datetime.time(8, 0, 0))
        TimeRangeFilterModel.objects.create(id=4, time=datetime.time(8, 0, 0))
        TimeRangeFilterModel.objects.create(id=5, time=datetime.time(8, 0, 0))
        TimeRangeFilterModel.objects.create(id=6, time=datetime.time(15, 15, 15))
        TimeRangeFilterModel.objects.create(id=7, time=datetime.time(18, 30))

    def setup_typed_choice_filter_model(self):
        print('Setup TypedChoiceFilterModel')

        TypedChoiceFilterModel.objects.create(id=1, text='1')
        TypedChoiceFilterModel.objects.create(id=2, text='One')
        TypedChoiceFilterModel.objects.create(id=3, text='one')
        TypedChoiceFilterModel.objects.create(id=4, text='2')
        TypedChoiceFilterModel.objects.create(id=5, text='Two')
        TypedChoiceFilterModel.objects.create(id=6, text='Not a Number')
        TypedChoiceFilterModel.objects.create(id=7, text='3.3')
        TypedChoiceFilterModel.objects.create(id=8)

    def setup_typed_multiple_choice_filter_model(self):
        print('Setup TypedMultipleChoiceFilterModel')

        TypedMultipleChoiceFilterModel.objects.create(id=1, text='1')
        TypedMultipleChoiceFilterModel.objects.create(id=2, text='One')
        TypedMultipleChoiceFilterModel.objects.create(id=3, text='2')
        TypedMultipleChoiceFilterModel.objects.create(id=4, text='2')
        TypedMultipleChoiceFilterModel.objects.create(id=5, text='Not a Number')
        TypedMultipleChoiceFilterModel.objects.create(id=6, text='3')
        TypedMultipleChoiceFilterModel.objects.create(id=7, text='3.3')
        TypedMultipleChoiceFilterModel.objects.create(id=8)

    def setup_uuid_filter_model(self):
        print('Setup UUIDFilterModel')

        UUIDFilterModel.objects.create(id=1, uuid='40828e84-66c7-46ee-a94a-1f2087970a68')
        UUIDFilterModel.objects.create(id=2, uuid='8f3ba455-2fbd-4f7b-82ff-12b05c0676e7')
        UUIDFilterModel.objects.create(id=3, uuid='df4078eb-67ca-49fe-b86d-742e0feaf3ad')
        UUIDFilterModel.objects.create(id=4, uuid='4275cc61-433a-44b2-8468-9cdfb149bb5e')
        UUIDFilterModel.objects.create(id=5, uuid='3b56ee7b-6fba-4ed6-9a1c-f08690b2a7f2')
        UUIDFilterModel.objects.create(id=6, uuid='46390e95-b41a-48ec-819a-3fa54b740d4d')
