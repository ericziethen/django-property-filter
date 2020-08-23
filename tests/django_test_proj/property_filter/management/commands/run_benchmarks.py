'''
TODO - FEATURES

    - Script Calls
        - 1000 Entries
        - 10000 Entries
        - 50000 Entries
        - 100000 Entries

    - Script Arguments
        - Number of Database Entries

    - Batch Script to call it, so can easily change the Database Used, and call both
    - Benchmark Model to Run Against
    - Multiple Databases (Sqlits + postgresql)
    - Multiple Number Database Entries
    - Multiple Datatypes
    - Multiple Filter Types (Single and Multiple Choice Ones)
    - Many (Single Filters) and Few (Multiple Filters) results
    - Compare Timing Filter & PropertyFilter
 
    - Tests
        - Single

    - LOGGING:
        - Log which Database is used

    FilterCombinations
        - Single Filter (NumberFilter)
        - Single Filter (CharFilter)
        - Single Filter (MultipleChoiceFilter AND)
        - Single Filter (MultipleChoiceFilter OR)
        - Mixed Filter (Number and Char Filter)
        - Mixed Filter (Number, Char Filter, Multiple Choice Filters)
        - Mixed Filter (5 Filters)

        call:TimeFilterAndPropetime_filters

    - CSV Output (1 Row per test scenario)
        - Date/Time
        - PropertyFilter Version used
        - Database Used
        - Database Entries
        - Results Found
        - Filters Used
        - Number of Fields Filtered
        - Filters Timing
        - Property Timing



    TimeFilterAndPropetime_filters(filter_dic, property_filter_dic, ???)  filter_dic/property_filter_dic = {'filter_name': lookup_value, 'name2': lookup_value...}
        time filterset.qs
        time propertyfilterset.qs
        log timing
'''

import configparser
import logging
import os
import sys

sys.path.insert(1, '../../')  # Find our main project

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from django_property_filter.utils import get_db_vendor, get_db_version

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('db_entries', type=int)
        parser.add_argument('csv_out_path', type=str)

    def handle(self, *args, **options):  # pylint: disable=too-many-locals,too-many-branches
        csv_path = options['csv_out_path']
        db_entries = options['db_entries']

        # Single Test Entry
        test_dic = {}
        test_dic['date/time'] = timezone.now()
        test_dic['version'] = get_plugin_version()
        test_dic['database'] = F'{get_db_vendor()} ({get_db_version()})'
        test_dic['db_entries'] = db_entries

        append_data_to_csv(csv_path, test_dic)

def append_data_to_csv(csv_file_path, data):
        print(data)


def get_plugin_version():
    config = configparser.RawConfigParser()
    config.read('../../setup.cfg')
    version = config.get('metadata', 'version')
    return version
