=======================
Development and Testing
=======================

Run the Test Suite locally
--------------------------

For running tests using sqlite use either

.. code-block:: batch

    Windows: $ dev\run_tests.bat sqlite
    Linux:   $ dev/run_tests.sh sqlite

or for postgresql (needs local postgres setup first)

.. code-block:: batch

    Windows: $ dev\run_tests.bat postgres-local
    Linux:   $ dev/run_tests.sh postgres-local

Run the Linters
---------------

.. code-block:: batch

    Windows: $ dev\run_linters.bat
    Linux:   $ dev/run_linters.sh


Run the Django Test Project
---------------------------

Change to the test project directory setup and run the django project

.. code-block:: batch

    $ cd tests\django_test_proj
    $ python manage.py migrate
    $ python manage.py setup_data
    $ python manage.py runserver

By default sqlite is used, but postgresql is also supported. For this set the
environment variable to the local postgres settings
    DJANGO_SETTINGS_MODULE=django_test_proj.settings_postgres_local
