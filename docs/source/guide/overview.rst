========
Overview
========

Limitations
-----------

.. warning::
    Because this app preserved Django Filtersets and filters them agains fields
    that are not Database fields all filtering happens in memory.
    Compared with direct sql optimized queries that might be slower and more
    memory intensive.

Database Parameter Limits
^^^^^^^^^^^^^^^^^^^^^^^^^

In theory there is no limit for most databases how many results can be returned
from a filter query unless the database implements a limit which will impact how
many results django-property-filter can return.

**sqlite**

.. warning::
    Sqlite3 defines SQLITE_MAX_VARIABLE_NUMBER which is a limit for parameters
    passed to a query.

    Depending on the version this limit might differ.
    By default from version 3.32.0 onwards have a default of 32766 while
    versions before this the limit was 999.

    See "Maximum Number Of Host Parameters In A Single SQL Statement" at
    https://www.sqlite.org/limits.html for further details.

Django-property-filter will try to return all values if possible, but if not
possible it will try to return as many as possible and log a warning message
similar to::
    WARNING:root:Only returning the first 3746 items because of max parameter limitations of Database "sqlite" with version "3.31.1"

It is possible to set a custom limit via the environment variable
"USER_DB_MAX_PARAMS". For example the user uses a custom compiled sqlite
version with a different than the default value for SQLITE_MAX_VARIABLE_NUMBER
the setting "USER_DB_MAX_PARAMS" to that value will use this value as a
fallback rather than default values.
