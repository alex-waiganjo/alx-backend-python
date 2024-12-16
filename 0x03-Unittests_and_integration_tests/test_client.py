#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import PropertyMock
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', return_value={"payload": True})
    def test_org(self, org_name: str, mock_get_json) -> None:

        # Github instance
        client = GithubOrgClient(org_name)

        # Mocking
        self.assertEqual(client.org, {"payload": True})

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self) -> None:

        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://test.com"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://test.com")

    @patch('client.get_json',
           return_value=[{"name": "repo1"}, {"name": "repo2"}])
    def test_public_repos(self, mock_get_json) -> None:

        mock_url = "http://api.github.com/orgs/google/repos"
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock,
                   return_value=mock_url) as mock_public_repos_url:
            client = GithubOrgClient('google')
            repos = client.public_repos()

            self.assertEqual(repos, ['repo1', 'repo2'])

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_url)

    @parameterized.expand([
        ({"key": "my_license"}, "my_license", True),
        ({"key": "other_license"}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict[str, Dict],
                         license_key: str, expected: bool) -> None:

        self.assertEqual(GithubOrgClient.has_license(repo, license_key),
                         expected)
