#!/usr/bin/env python3
from client import GithubOrgClient
import unittest
from unittest.mock import patch
from parameterized import parameterized


import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        # Set the mock to return a dummy dict
        mock_get_json.return_value = {"org": org_name}

        # Instantiate client
        client = GithubOrgClient(org_name)

        # Call .org() method
        result = client.org

        # Assert get_json called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Assert .org() returns what mock_get_json returns
        self.assertEqual(result, {"org": org_name})


if __name__ == "__main__":
    unittest.main()
