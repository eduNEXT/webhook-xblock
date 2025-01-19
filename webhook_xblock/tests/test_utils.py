"""Tests for the utils module."""
from unittest import TestCase

from webhook_xblock.utils import flatten_dict


class TestUtils(TestCase):
    """Unit tests for the utility functions."""

    def test_flatten_dict(self):
        """Test that flatten_dict flattens a nested dictionary."""
        nested_dict = {
            "a": {
                "b": {
                    "c": 1
                },
                "d": 2
            },
            "e": 3,
        }
        expected = {"a_b_c": 1, "a_d": 2, "e": 3}

        result = flatten_dict(nested_dict)

        self.assertEqual(result, expected)
