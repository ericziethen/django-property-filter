
import logging

from django_property_filter import PropertyNumberFilter


def test_label_set():
    my_filter_label = PropertyNumberFilter(label='test label', field_name='field_name', lookup_expr='gte')
    assert my_filter_label.label == 'test label'

    my_filter_no_label = PropertyNumberFilter(field_name='field_name', lookup_expr='gte')
    assert my_filter_no_label.label == 'field_name [gte]'

def test_handle_invalid_type_comparison(caplog):

    num_filter = PropertyNumberFilter(field_name='field_name', lookup_expr='lt')

    with caplog.at_level(logging.DEBUG):
        result = num_filter._compare_lookup_with_qs_entry(num_filter.lookup_expr, 'text', 15)

        assert not result
        assert 'Error during comparing ' in caplog.text
