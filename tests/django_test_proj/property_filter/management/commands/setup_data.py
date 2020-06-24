
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware

from property_filter.models import (
    BooleanFilterModel,
    DateFilterModel,
    DateFromToRangeFilterModel,
    DateTimeFilterModel,
    DurationFilterModel,
    RangeFilterModel,
    NumberFilterModel,
    CharFilterModel,
    TimeFilterModel,
    TimeClass,

)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Setup RangeFilterModel')
        for num in range(21):
            RangeFilterModel.objects.update_or_create(number=num)

        # BooleanFilterModel Data
        print('Setup BooleanFilterModel')
        BooleanFilterModel.objects.update_or_create(id=1, is_true=True)
        BooleanFilterModel.objects.update_or_create(id=2, is_true=False)
        BooleanFilterModel.objects.update_or_create(id=3, )
        BooleanFilterModel.objects.update_or_create(id=4, is_true=True)
        BooleanFilterModel.objects.update_or_create(id=5, is_true=False)
        BooleanFilterModel.objects.update_or_create(id=6, )

        # CharFilterModel Data
        print('Setup CharFilterModel')
        CharFilterModel.objects.update_or_create(id=1, name='Tom')
        CharFilterModel.objects.update_or_create(id=2, name='Peter')
        CharFilterModel.objects.update_or_create(id=3, name='Ralph')
        CharFilterModel.objects.update_or_create(id=4, name='Tom')
        CharFilterModel.objects.update_or_create(id=5, name='TOM')
        CharFilterModel.objects.update_or_create(id=6, name='Tom')
        CharFilterModel.objects.update_or_create(id=7)
        CharFilterModel.objects.update_or_create(id=8)

        # DateFilterModel Data
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

        # TimeClass Data
        print('Setup TimeClass')
        TimeClass.objects.update_or_create(id=1, time=datetime.time(7, 30, 15))
        TimeClass.objects.update_or_create(id=2, time=datetime.time(7, 30, 15))
        TimeClass.objects.update_or_create(id=3, time=datetime.time(8, 0, 0))
        TimeClass.objects.update_or_create(id=4, time=datetime.time(8, 0, 0))
        TimeClass.objects.update_or_create(id=5, time=datetime.time(8, 0, 0))
        TimeClass.objects.update_or_create(id=6, time=datetime.time(15, 15, 15))
        TimeClass.objects.update_or_create(id=7, time=datetime.time(18, 30))

        # DurationFilterModel Data
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

        # DateTimeFilterModel Data
        print('Setup DateTimeFilterModel')
        DateTimeFilterModel.objects.update_or_create(id=1, date_time=make_aware(datetime.datetime(2020, 1, 1, 13, 30)))
        DateTimeFilterModel.objects.update_or_create(id=2, date_time=make_aware(datetime.datetime(2020, 1, 1, 13, 40)))
        DateTimeFilterModel.objects.update_or_create(id=3, date_time=make_aware(datetime.datetime(2020, 2, 2, 12)))
        DateTimeFilterModel.objects.update_or_create(id=4, date_time=make_aware(datetime.datetime(2020, 2, 2, 12, 0)))
        DateTimeFilterModel.objects.update_or_create(id=5, date_time=make_aware(datetime.datetime(2020, 2, 2, 12, 0, 0)))
        DateTimeFilterModel.objects.update_or_create(id=6, date_time=make_aware(datetime.datetime(2021, 1, 1, 13, 30)))
        DateTimeFilterModel.objects.update_or_create(id=7, date_time=make_aware(datetime.datetime(2021, 1, 1, 13, 30)))
        DateTimeFilterModel.objects.update_or_create(id=8, date_time=make_aware(datetime.datetime(2022, 1, 1, 13, 30)))

        ##### FILTER SPECIFIC CLASSES #####

        self.setup_date_from_to_range_filter_model()
        self.setup_number_filter_model()
        self.setup_time_filter_model()

        # Finished
        print('Setup Finished')

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

    def setup_number_filter_model(self):
        print('Setup NumberFilterModel')

        for num in range(21):
            NumberFilterModel.objects.update_or_create(number=num)

    def setup_time_filter_model(self):
        print('Setup TimeFilterModel')

        TimeFilterModel.objects.update_or_create(id=1, time=datetime.time(7, 30, 15))
        TimeFilterModel.objects.update_or_create(id=2, time=datetime.time(7, 30, 15))
        TimeFilterModel.objects.update_or_create(id=3, time=datetime.time(8, 0, 0))
        TimeFilterModel.objects.update_or_create(id=4, time=datetime.time(8, 0, 0))
        TimeFilterModel.objects.update_or_create(id=5, time=datetime.time(8, 0, 0))
        TimeFilterModel.objects.update_or_create(id=6, time=datetime.time(15, 15, 15))
        TimeFilterModel.objects.update_or_create(id=7, time=datetime.time(18, 30))

