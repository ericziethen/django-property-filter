import os

from django_property_filter import project_logger


def test_logging():
    log_dir = R'django_property_filter\logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    project_logger.setup_logger(R'django_property_filter\logs\test_log.txt')
    project_logger.test_logging()
