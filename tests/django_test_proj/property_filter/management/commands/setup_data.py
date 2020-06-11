
import datetime

from django.core.management.base import BaseCommand

from property_filter.models import (
    BooleanClass,
    DateClass,
    NumberClass,
    TextClass,
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Setup NumberClass')
        for num in range(21):
            NumberClass.objects.update_or_create(number=num)

        # BooleanClass Data
        print('Setup BooleanClass')
        BooleanClass.objects.update_or_create(id=1, is_true=True)
        BooleanClass.objects.update_or_create(id=2, is_true=False)
        BooleanClass.objects.update_or_create(id=3, )
        BooleanClass.objects.update_or_create(id=4, is_true=True)
        BooleanClass.objects.update_or_create(id=5, is_true=False)
        BooleanClass.objects.update_or_create(id=6, )

        # TextClass Data
        print('Setup TextClass')
        TextClass.objects.update_or_create(id=1, name='Tom')
        TextClass.objects.update_or_create(id=2, name='Peter')
        TextClass.objects.update_or_create(id=3, name='Ralph')
        TextClass.objects.update_or_create(id=4, name='Tom')
        TextClass.objects.update_or_create(id=5, name='TOM')
        TextClass.objects.update_or_create(id=6, name='Tom')
        TextClass.objects.update_or_create(id=7)
        TextClass.objects.update_or_create(id=8)

        # DateClass Data
        print('Setup DateClass')
        DateClass.objects.update_or_create(id=1, date=datetime.date(2018, 2, 1))
        DateClass.objects.update_or_create(id=2, date=datetime.date(2019, 3, 2))
        DateClass.objects.update_or_create(id=3, date=datetime.date(2019, 3, 2))
        DateClass.objects.update_or_create(id=4, date=datetime.date(2019, 3, 4))
        DateClass.objects.update_or_create(id=5, date=datetime.date(2020, 2, 5))
        DateClass.objects.update_or_create(id=6, date=datetime.date(2020, 2, 6))
        DateClass.objects.update_or_create(id=7, date=datetime.date(2020, 2, 6))
        DateClass.objects.update_or_create(id=8, date=datetime.date(2020, 2, 6))
        DateClass.objects.update_or_create(id=9, date=datetime.date(2020, 2, 9))

        # Finished
        print('Setup Finished')
