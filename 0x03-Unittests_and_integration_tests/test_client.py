#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that .org property returns the correct org payload."""
        test_payload = {"org": org_name}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)
        
        # First call - should call get_json
        self.assertEqual(client.org, test_payload)
        # Second call - should use memoized value
        self.assertEqual(client.org, test_payload)
        
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url property returns correct repos URL."""
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            test_url = "https://api.github.com/orgs/testorg/repos"
            mock_org.return_value = {"repos_url": test_url}
            
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, test_url)
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_repos_payload(self, mock_get_json):
        """Test repos_payload returns the correct payload."""
        mock_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = mock_payload
        
        with patch('client.GithubOrgClient._public_repos_url', 
                  new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://example.com/repos"
            client = GithubOrgClient("testorg")
            
            # First call
            self.assertEqual(client.repos_payload, mock_payload)
            # Second call (memoized)
            self.assertEqual(client.repos_payload, mock_payload)
            
            mock_get_json.assert_called_once_with("https://example.com/repos")

    @patch('client.GithubOrgClient.repos_payload', new_callable=PropertyMock)
    def test_public_repos(self, mock_repos_payload):
        """Test public_repos() returns a list of repository names."""
        mock_repos_payload.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])
        self.assertEqual(client.public_repos("apache-2.0"), ["repo2"])
        mock_repos_payload.assert_called()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": {}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test static method has_license returns correct boolean."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get before all tests."""
        cls.get_patcher = patch('client.get_json')  # Patch get_json instead
        cls.mock_get_json = cls.get_patcher.start()

        def org_side_effect(url):
            if url.endswith("/orgs/test_org"):
                return cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            return None

        cls.mock_get_json.side_effect = org_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos() returns expected repo names."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)
        # Should call get_json twice (org and repos_payload)
        self.assertEqual(self.mock_get_json.call_count, 2)

    def test_public_repos_with_license(self):
        """Test public_repos() filters repos by license."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()