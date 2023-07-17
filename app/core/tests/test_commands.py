"""
Test custom Django managment commands.
"""
# Mock the behaviour of the db
from unittest.mock import patch

# Possible error we can get while trying to connect to the db
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError

# Function provided by django to simulate calling a command by the name
from django.core.management import call_command
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
# BaseCommand has a check method that 'Command' inherits
# to check the status of the database, in order to mock it's response
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_to_wait_for_db_ready(self, patched_check):
        """Test waiting for db if db ready."""
        # Simulate that the check method returns True
        patched_check.return_value = True

        # Also check if the command is corectly set up
        call_command("wait_for_db")

        # Checks if it connects to the db that we refered as
        # 'default' in settings.py
        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    # Argumetns patch order, from bottom to top,
    # from the inside-out (method to class)
    def test_wait_fir_db_delay(self, patched_sleep, patched_check):
        """Test waiting for the database when getting OperationalError"""
        # Patch exeption raising as if the database wasn't ready
        # The first 2 times we call the mock,
        # we want to raise the Psycopg2Error
        #   --> Occurs when postgres itself has not started yet,
        #       thus it's not ready to connect
        # The 3 following times, we're raising an OperationalError
        #   --> Occurs when the db is rdy to accept connections but
        #       has not yet set up the testing db we want to use
        # The last time it returns True
        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        # Check that the patch is called 6 times the method
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
