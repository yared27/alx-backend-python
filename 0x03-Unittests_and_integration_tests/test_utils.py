#!/usr/bin/env python3
"""
Unit tests for utils module: access_nested_map, get_json, and memoize.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json
from unittest.mock import patch
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({"a": {"b": {"c": 3}}}, ("a", "b", "c"), 3),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the correct value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """Tests for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, url, expected_payload):
        """Test that get_json returns the expected JSON data."""
        with patch("utils.requests.get") as mock_get:
            mock_get.return_value.json.return_value = expected_payload
            result = get_json(url)
            self.assertEqual(result, expected_payload)
            mock_get.assert_called_once_with(url)

class TestMemoize(unittest.TestCase):
    def test_memoize(self):

        class TestClass:
            def a_method(self):
                return 42
            @memoize
            def a_property(self):
                return self.a_method()
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            restult1 = obj.a_property()
            result2 = obj.a_property()
            self.assertEqual(restult1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
