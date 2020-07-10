
import datetime

from django.db import transaction
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware

from property_filter.models import (
    AllValuesFilterModel,
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
    ModelChoiceFilterModel,
    ModelChoiceFilterRelatedModel,
    NumberFilterModel,
    RangeFilterModel,
    TimeFilterModel,
    TimeRangeFilterModel,
    TypedChoiceFilterModel,
    UUIDFilterModel,
)


class Command(BaseCommand):

    def handle(self, *args, **options):

        with transaction.atomic():
            self.setup_all_values_filter_model()
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
            self.setup_model_choice_filter_model()
            self.setup_number_filter_model()
            self.setup_range_filter_model()
            self.setup_time_filter_model()
            self.setup_time_range_filter_model()
            self.setup_typed_choice_filter_model()
            self.setup_uuid_filter_model()

        print('>> Setup Finished')

    def setup_all_values_filter_model(self):
        print('Setup AllValuesFilterModel')

        AllValuesFilterModel.objects.update_or_create(id=-1, number=-1)
        AllValuesFilterModel.objects.update_or_create(id=0, number=0)
        AllValuesFilterModel.objects.update_or_create(id=1, number=1)
        AllValuesFilterModel.objects.update_or_create(id=2, number=2)
        AllValuesFilterModel.objects.update_or_create(id=3, number=2)
        AllValuesFilterModel.objects.update_or_create(id=4, number=2)
        AllValuesFilterModel.objects.update_or_create(id=5, number=3)
        AllValuesFilterModel.objects.update_or_create(id=6, number=4)
        AllValuesFilterModel.objects.update_or_create(id=7, number=10)
        AllValuesFilterModel.objects.update_or_create(id=8, number=20)
        AllValuesFilterModel.objects.update_or_create(id=9)

    def setup_boolean_filter_model(self):
        print('Setup BooleanFilterModel')

        BooleanFilterModel.objects.update_or_create(id=1, is_true=True)
        BooleanFilterModel.objects.update_or_create(id=2, is_true=False)
        BooleanFilterModel.objects.update_or_create(id=3, )
        BooleanFilterModel.objects.update_or_create(id=4, is_true=True)
        BooleanFilterModel.objects.update_or_create(id=5, is_true=False)
        BooleanFilterModel.objects.update_or_create(id=6, )

    def setup_char_filter_model(self):
        print('Setup CharFilterModel')

        CharFilterModel.objects.update_or_create(id=1, name='Tom')
        CharFilterModel.objects.update_or_create(id=2, name='Peter')
        CharFilterModel.objects.update_or_create(id=3, name='Ralph')
        CharFilterModel.objects.update_or_create(id=4, name='Tom')
        CharFilterModel.objects.update_or_create(id=5, name='TOM')
        CharFilterModel.objects.update_or_create(id=6, name='Tom')
        CharFilterModel.objects.update_or_create(id=7)
        CharFilterModel.objects.update_or_create(id=8)

    def setup_choice_filter_model(self):
        print('Setup ChoiceFilterModel')

        ChoiceFilterModel.objects.update_or_create(id=-1, number=-1)
        ChoiceFilterModel.objects.update_or_create(id=0, number=0)
        ChoiceFilterModel.objects.update_or_create(id=1, number=1)
        ChoiceFilterModel.objects.update_or_create(id=2, number=2)
        ChoiceFilterModel.objects.update_or_create(id=3, number=2)
        ChoiceFilterModel.objects.update_or_create(id=4, number=2)
        ChoiceFilterModel.objects.update_or_create(id=5, number=3)
        ChoiceFilterModel.objects.update_or_create(id=6, number=4)
        ChoiceFilterModel.objects.update_or_create(id=7, number=10)
        ChoiceFilterModel.objects.update_or_create(id=8, number=20)
        ChoiceFilterModel.objects.update_or_create(id=9)

    def setup_date_filter_model(self):
        print('Setup DateFilterModel')

        DateFilterModel.objects.update_or_create(id=1, date=datetime.date(2018, 2, 1))
        DateFilterModel.objects.update_or_create(id=2, date=datetime.date(2019, 3, 2))
        DateFilterModel.objects.update_or_create(id=3, date=datetime.date(2019, 3, 2))
        DateFilterModel.objects.update_or_create(id=4, date=datetime.date(2019, 3, 4))
        DateFilterModel.objects.update_or_create(id=5, date=datetime.date(2020, 2, 5))
        DateFilterModel.objects.update_or_create(id=6, date=datetime.date(2020, 2, 6))
        DateFilterModel.objects.update_or_create(id=7, date=datetime.date(2020, 2, 6))
        DateFilterModel.objects.update_or_create(id=8, date=datetime.date(2020, 2, 6))
        DateFilterModel.objects.update_or_create(id=9, date=datetime.date(2020, 2, 9))

    def setup_date_from_to_range_filter_model(self):
        print('Setup DateFromToRangeFilterModel')

        tz = timezone.get_default_timezone()

        DateFromToRangeFilterModel.objects.update_or_create(
            id=-1,
            date=datetime.date(2018, 2, 1),
            date_time=datetime.datetime(2018, 2, 1, 13, 30, tzinfo=tz))
        DateFromToRangeFilterModel.objects.update_or_create(
            id=0,
            date=datetime.date(2019, 3, 2),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        DateFromToRangeFilterModel.objects.update_or_create(
            id=1,
            date=datetime.date(2019, 3, 2),
            date_time=datetime.datetime(2019, 3, 2, 12, tzinfo=tz))
        DateFromToRangeFilterModel.objects.update_or_create(
            id=2,
            date=datetime.date(2019, 3, 4),
            date_time=datetime.datetime(2019, 3, 4, 12, 0, tzinfo=tz))
        DateFromToRangeFilterModel.objects.update_or_create(
            id=3,
            date=datetime.date(2020, 2, 5),
            date_time=datetime.datetime(2020, 2, 5, 12, 0, 0, tzinfo=tz))
        DateFromToRangeFilterModel.objects.update_or_create(
            id=4,
            date=datetime.date(2020, 2, 6),
            date_time=datetime.datetime(2020, 2, 6, 13, 30, tzinfo=tz))

    def setup_date_range_filter_model(self):
        print('Setup DateRangeFilterModel')

        tz = timezone.get_default_timezone()

        DateRangeFilterModel.objects.update_or_create(
            id=-1,
            date=datetime.date.today(),
            date_time=datetime.datetime.now(tz=tz))

        DateRangeFilterModel.objects.update_or_create(
            id=0,
            date=datetime.date.today() - datetime.timedelta(days=1),
            date_time=datetime.datetime.now(tz=tz) - datetime.timedelta(days=1))

        DateRangeFilterModel.objects.update_or_create(
            id=1,
            date=datetime.date.today() - datetime.timedelta(days=6),
            date_time=datetime.datetime.now(tz=tz) - datetime.timedelta(days=6))

        DateRangeFilterModel.objects.update_or_create(
            id=2,
            date=datetime.date.today() - datetime.timedelta(days=7),
            date_time=datetime.datetime.now(tz=tz) - datetime.timedelta(days=7))

        DateRangeFilterModel.objects.update_or_create(
            id=3,
            date=datetime.date.today() - datetime.timedelta(days=15),
            date_time=datetime.datetime.now(tz=tz) - datetime.timedelta(days=15))

        DateRangeFilterModel.objects.update_or_create(
            id=4,
            date=datetime.date.today() + datetime.timedelta(days=15),
            date_time=datetime.datetime.now(tz=tz) + datetime.timedelta(days=15))

        DateRangeFilterModel.objects.update_or_create(
            id=5,
            date=datetime.date.today() + datetime.timedelta(days=400),
            date_time=datetime.datetime.now(tz=tz) + datetime.timedelta(days=400))

        DateRangeFilterModel.objects.update_or_create(
            id=6,
            date=datetime.date.today() - datetime.timedelta(days=800),
            date_time=datetime.datetime.now(tz=tz) - datetime.timedelta(days=800))

    def setup_date_time_filter_model(self):
        print('Setup DateTimeFilterModel')

        DateTimeFilterModel.objects.update_or_create(id=1, date_time=make_aware(datetime.datetime(2020, 1, 1, 13, 30)))
        DateTimeFilterModel.objects.update_or_create(id=2, date_time=make_aware(datetime.datetime(2020, 1, 1, 13, 40)))
        DateTimeFilterModel.objects.update_or_create(id=3, date_time=make_aware(datetime.datetime(2020, 2, 2, 12)))
        DateTimeFilterModel.objects.update_or_create(id=4, date_time=make_aware(datetime.datetime(2020, 2, 2, 12, 0)))
        DateTimeFilterModel.objects.update_or_create(id=5, date_time=make_aware(datetime.datetime(2020, 2, 2, 12, 0, 0)))
        DateTimeFilterModel.objects.update_or_create(id=6, date_time=make_aware(datetime.datetime(2021, 1, 1, 13, 30)))
        DateTimeFilterModel.objects.update_or_create(id=7, date_time=make_aware(datetime.datetime(2021, 1, 1, 13, 30)))
        DateTimeFilterModel.objects.update_or_create(id=8, date_time=make_aware(datetime.datetime(2022, 1, 1, 13, 30)))

    def setup_date_time_from_to_range_filter_model(self):
        print('Setup DateTimeFromToRangeFilterModel')

        DateTimeFromToRangeFilterModel.objects.update_or_create(id=1, date_time=make_aware(datetime.datetime(2020, 1, 1, 13, 30)))
        DateTimeFromToRangeFilterModel.objects.update_or_create(id=2, date_time=make_aware(datetime.datetime(2020, 1, 1, 13, 40)))
        DateTimeFromToRangeFilterModel.objects.update_or_create(id=3, date_time=make_aware(datetime.datetime(2020, 2, 2, 12)))
        DateTimeFromToRangeFilterModel.objects.update_or_create(id=4, date_time=make_aware(datetime.datetime(2020, 2, 2, 12, 0)))
        DateTimeFromToRangeFilterModel.objects.update_or_create(id=5, date_time=make_aware(datetime.datetime(2020, 2, 2, 12, 0, 0)))
        DateTimeFromToRangeFilterModel.objects.update_or_create(id=6, date_time=make_aware(datetime.datetime(2021, 1, 1, 13, 30)))
        DateTimeFromToRangeFilterModel.objects.update_or_create(id=7, date_time=make_aware(datetime.datetime(2021, 1, 1, 13, 30)))
        DateTimeFromToRangeFilterModel.objects.update_or_create(id=8, date_time=make_aware(datetime.datetime(2022, 1, 1, 13, 30)))

    def setup_duration_filter_model(self):
        print('Setup DurationFilterModel')

        DurationFilterModel.objects.update_or_create(id=1, duration=datetime.timedelta(hours=5))
        DurationFilterModel.objects.update_or_create(id=2, duration=datetime.timedelta(hours=5))
        DurationFilterModel.objects.update_or_create(id=3, duration=datetime.timedelta(days=1, hours=10))
        DurationFilterModel.objects.update_or_create(id=4, duration=datetime.timedelta(days=2, hours=10))
        DurationFilterModel.objects.update_or_create(id=5, duration=datetime.timedelta(days=2, hours=10))
        DurationFilterModel.objects.update_or_create(id=6, duration=datetime.timedelta(days=15))
        DurationFilterModel.objects.update_or_create(id=7, duration=datetime.timedelta(days=15))
        DurationFilterModel.objects.update_or_create(id=8, duration=datetime.timedelta(days=30))
        DurationFilterModel.objects.update_or_create(id=9, duration=datetime.timedelta(days=200))

    def setup_iso_date_time_filter_model(self):
        print('Setup IsoDateTimeFilterModel')

        IsoDateTimeFilterModel.objects.update_or_create(id=1, date_time='2020-01-03T12:00:00+12:00')
        IsoDateTimeFilterModel.objects.update_or_create(id=2, date_time='2020-01-03T12:00:00+11:00')
        IsoDateTimeFilterModel.objects.update_or_create(id=3, date_time='2020-01-03T12:00:00+10:00')
        IsoDateTimeFilterModel.objects.update_or_create(id=4, date_time='2020-12-03T12:00:00+10:00')
        IsoDateTimeFilterModel.objects.update_or_create(id=5, date_time='2020-12-03T12:00:00+10:00')
        IsoDateTimeFilterModel.objects.update_or_create(id=6, date_time='2021-12-03T12:00:00+10:00')

    def setup_iso_date_time_from_to_range_filter_model(self):
        print('Setup IsoDateTimeFromToRangeFilterModel')

        IsoDateTimeFromToRangeFilterModel.objects.update_or_create(id=1, date_time='2020-01-03T12:00:00+12:00')
        IsoDateTimeFromToRangeFilterModel.objects.update_or_create(id=2, date_time='2020-01-03T12:00:00+11:00')
        IsoDateTimeFromToRangeFilterModel.objects.update_or_create(id=3, date_time='2020-01-03T12:00:00+10:00')
        IsoDateTimeFromToRangeFilterModel.objects.update_or_create(id=4, date_time='2020-12-03T12:00:00+10:00')
        IsoDateTimeFromToRangeFilterModel.objects.update_or_create(id=5, date_time='2020-12-03T12:00:00+10:00')
        IsoDateTimeFromToRangeFilterModel.objects.update_or_create(id=6, date_time='2021-12-03T12:00:00+10:00')

    def setup_model_choice_filter_model(self):
        print('Setup ModelChoiceFilterModel')

        (related_a, _) = ModelChoiceFilterRelatedModel.objects.update_or_create(id=1, text='AAA')
        (related_b, _) = ModelChoiceFilterRelatedModel.objects.update_or_create(id=2, text='BBB')
        (related_c, _) = ModelChoiceFilterRelatedModel.objects.update_or_create(id=3, text='CCC')

        ModelChoiceFilterModel.objects.update_or_create(id=1, related=related_a)
        ModelChoiceFilterModel.objects.update_or_create(id=2, related=related_a)
        ModelChoiceFilterModel.objects.update_or_create(id=3, related=related_a)
        ModelChoiceFilterModel.objects.update_or_create(id=4, related=related_c)
        ModelChoiceFilterModel.objects.update_or_create(id=5, related=related_c)


    def setup_number_filter_model(self):
        print('Setup NumberFilterModel')

        for num in range(21):
            NumberFilterModel.objects.update_or_create(number=num)

    def setup_range_filter_model(self):
        print('Setup RangeFilterModel')

        for num in range(21):
            RangeFilterModel.objects.update_or_create(number=num)

    def setup_time_filter_model(self):
        print('Setup TimeFilterModel')

        TimeFilterModel.objects.update_or_create(id=1, time=datetime.time(7, 30, 15))
        TimeFilterModel.objects.update_or_create(id=2, time=datetime.time(7, 30, 15))
        TimeFilterModel.objects.update_or_create(id=3, time=datetime.time(8, 0, 0))
        TimeFilterModel.objects.update_or_create(id=4, time=datetime.time(8, 0, 0))
        TimeFilterModel.objects.update_or_create(id=5, time=datetime.time(8, 0, 0))
        TimeFilterModel.objects.update_or_create(id=6, time=datetime.time(15, 15, 15))
        TimeFilterModel.objects.update_or_create(id=7, time=datetime.time(18, 30))

    def setup_time_range_filter_model(self):
        print('Setup TimeRangeFilterModel')

        TimeRangeFilterModel.objects.update_or_create(id=1, time=datetime.time(7, 30, 15))
        TimeRangeFilterModel.objects.update_or_create(id=2, time=datetime.time(7, 30, 15))
        TimeRangeFilterModel.objects.update_or_create(id=3, time=datetime.time(8, 0, 0))
        TimeRangeFilterModel.objects.update_or_create(id=4, time=datetime.time(8, 0, 0))
        TimeRangeFilterModel.objects.update_or_create(id=5, time=datetime.time(8, 0, 0))
        TimeRangeFilterModel.objects.update_or_create(id=6, time=datetime.time(15, 15, 15))
        TimeRangeFilterModel.objects.update_or_create(id=7, time=datetime.time(18, 30))

    def setup_typed_choice_filter_model(self):
        print('Setup TypedChoiceFilterModel')

        TypedChoiceFilterModel.objects.update_or_create(id=1, text='1')
        TypedChoiceFilterModel.objects.update_or_create(id=2, text='One')
        TypedChoiceFilterModel.objects.update_or_create(id=3, text='2')
        TypedChoiceFilterModel.objects.update_or_create(id=4, text='Two')
        TypedChoiceFilterModel.objects.update_or_create(id=5, text='Not a Number')
        TypedChoiceFilterModel.objects.update_or_create(id=6, text='3.3')
        TypedChoiceFilterModel.objects.update_or_create(id=7)

    def setup_uuid_filter_model(self):
        print('Setup UUIDFilterModel')

        UUIDFilterModel.objects.update_or_create(id=1, uuid='40828e84-66c7-46ee-a94a-1f2087970a68')
        UUIDFilterModel.objects.update_or_create(id=2, uuid='8f3ba455-2fbd-4f7b-82ff-12b05c0676e7')
        UUIDFilterModel.objects.update_or_create(id=3, uuid='df4078eb-67ca-49fe-b86d-742e0feaf3ad')
        UUIDFilterModel.objects.update_or_create(id=4, uuid='4275cc61-433a-44b2-8468-9cdfb149bb5e')
        UUIDFilterModel.objects.update_or_create(id=5, uuid='3b56ee7b-6fba-4ed6-9a1c-f08690b2a7f2')
        UUIDFilterModel.objects.update_or_create(id=6, uuid='46390e95-b41a-48ec-819a-3fa54b740d4d')
