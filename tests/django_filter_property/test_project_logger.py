import os

from django_filter_property import project_logger


def test_logging():
    log_dir = R'django_filter_property\logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    project_logger.setup_logger(R'django_filter_property\logs\test_log.txt')
    project_logger.test_logging()
