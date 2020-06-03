
from django.core.management.base import BaseCommand

from property_filter.models import (
    BooleanClass,
    NumberClass,
    TextClass,
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for num in range(21):
            NumberClass.objects.update_or_create(number=num)

        # BooleanClass Data
        BooleanClass.objects.update_or_create(id=1, is_true=True)
        BooleanClass.objects.update_or_create(id=2, is_true=False)
        BooleanClass.objects.update_or_create(id=3, )
        BooleanClass.objects.update_or_create(id=4, is_true=True)
        BooleanClass.objects.update_or_create(id=5, is_true=False)
        BooleanClass.objects.update_or_create(id=6, )

        # TextClass Data
        TextClass.objects.update_or_create(id=1, name='Tom')
        TextClass.objects.update_or_create(id=2, name='Peter')
        TextClass.objects.update_or_create(id=3, name='Ralph')
        TextClass.objects.update_or_create(id=4, name='Tom')
        TextClass.objects.update_or_create(id=5, name='TOM')
        TextClass.objects.update_or_create(id=6, name='Tom')
        TextClass.objects.update_or_create(id=7)
        TextClass.objects.update_or_create(id=8)



        print('BEFORE PRAGMA')
        qs = TextClass.objects.filter(name__contains='Tom')
        print('  contains "Tom"', qs.query, qs)
        qs = TextClass.objects.filter(name__icontains='Tom')
        print('  icontains "Tom"', qs.query, qs)

        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute('PRAGMA case_sensitive_like = true;')

        print('AFTER PRAGMA')
        qs = TextClass.objects.filter(name__contains='Tom')
        print('  contains "Tom"', qs.query, qs)
        qs = TextClass.objects.filter(name__icontains='Tom')
        print('  icontains "Tom"', qs.query, qs)
