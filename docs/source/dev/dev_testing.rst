=======================
Development and Testing
=======================

Run the Test Suite
------------------

.. code-block:: batch

    $ dev\run_tests.bat

Run the Linters
---------------

.. code-block:: batch

    $ dev\run_linters.bat


Run the Django Test Project
---------------------------

Change to the test project directory setup and run the django project

.. code-block:: batch

    $ cd tests\django_test_proj
    $ python manage.py migrate
    $ python manage.py setup_data
    $ python manage.py runserver
