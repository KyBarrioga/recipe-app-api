"""
Docstring for app.core.tests.test_commands
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.test import SimpleTestCase


@patch('core.management.commands.wait_db_buffer.Command.check')
class CommandTests(SimpleTestCase):
    """Tests for the custom Django management commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database when database is available."""
        patched_check.return_value = True

        call_command('wait_db_buffer')

        patched_check.assert_called_once_with(databases=['default'])

    @patch("time.sleep")
    def test_wait_for_db_not_ready(self, patched_sleep, patched_check):
        """Test waiting for database when database is not available."""
        patched_check.side_effect = [Psycopg2Error] * 5 + [True]

        call_command('wait_db_buffer')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
