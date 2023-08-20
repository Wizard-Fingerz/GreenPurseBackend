# run_tests_with_coverage.py

import os
import coverage
from django.core.management import execute_from_command_line

# Set up coverage
cov = coverage.Coverage()
cov.erase()
cov.start()

# Run Django tests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GreenPurseBackEnd.settings")  # Replace with your actual project settings module
execute_from_command_line(["manage.py", "test"])

# Stop coverage
cov.stop()
cov.save()
cov.report(show_missing=True)
