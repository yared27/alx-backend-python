#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({"a": {"b": {"c": 3}}}, ("a", "b", "c"), 3),
    ])
    def test_access_nested_map(self, input_map, path, expected):
        self.assertEqual(access_nested_map(input_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a":1},("a","b"))
    ])
    def test_access_nested_map_exception(self, input_map, path):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(input_map, path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")
            
