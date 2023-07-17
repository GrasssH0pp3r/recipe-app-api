"""
Calculator tests

No need for database => SimpleTestCase
"""
from django.test import SimpleTestCase
from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc module."""

    def test_add_numbers(self):
        """Test adding numbers together."""
        res = calc.add(5, 6)

        self.assertEqual(res, 11)

    def text_subtract_numbers(self):
        """Test subtracting numbers."""
        res = calc.subtract(9, 2)

        self.assertEqual(res, 7)
