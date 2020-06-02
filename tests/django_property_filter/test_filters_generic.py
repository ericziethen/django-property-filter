

from django_property_filter import PropertyNumberFilter


def test_label_set():
    my_filter_label = PropertyNumberFilter(label='test label', property_fld_name='field_name', lookup_expr='gte')
    assert my_filter_label.label == 'test label'

    my_filter_no_label = PropertyNumberFilter(property_fld_name='field_name', lookup_expr='gte')
    assert my_filter_no_label.label == 'field_name [gte]'
