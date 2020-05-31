
from django_filters import Filter, FilterSet


class PropertyFilterSet(FilterSet):

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        self._setup_property_filters()

    def _add_filter(self, filter_class, property_fld_name, lookup_expr):
        """Add a Filter."""
        filter_name = F'{property_fld_name}__{lookup_expr}'
        self.filters[filter_name] = filter_class(property_fld_name=property_fld_name, lookup_expr=lookup_expr)

    def _setup_property_filters(self):
        """Setup implicit filters."""
        if 'property_fields' in self.__class__.Meta.__dict__:
            prop_fields = self.__class__.Meta.__dict__['property_fields']

            for field in prop_fields:
                prop_fld_name = field[0]
                prop_filter_class = field[1]
                lookup_xpr_list = field[2]

                # Validate the attributes
                if not issubclass(prop_filter_class, Filter):
                    raise ValueError(F'{prop_filter_class} is not a subclass of {Filter}')

                if not isinstance(prop_fld_name, str):
                    raise ValueError(F'Property field "{prop_fld_name}" is not a str')

                if not isinstance(lookup_xpr_list, list) or not lookup_xpr_list:
                    raise ValueError(F'Lookup list "{lookup_xpr_list}" is not a valid list of lookups')

                # Create all Filters
                for lookup in lookup_xpr_list:
                    self._add_filter(prop_filter_class, prop_fld_name, lookup)
