#!/usr/bin/env python3

"""
Unit tests for the GithubOrgClient class in the client module.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_response, mock_get_json):
        """
        Test that GithubOrgClient.org calls get_json with the correct URL
        and returns the expected response.
        """
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_response)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the expected URL
        based on the mocked org payload.
        """
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/test-org/repos"
        }
        mock_org.return_value = mock_payload

        client = GithubOrgClient("test-org")
        result = client._public_repos_url
        expected = "https://api.github.com/orgs/test-org/repos"
        self.assertEqual(result, expected)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the expected list
        of repository names based on the mocked response.
        """
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_public_repos_url = "https://api.github.com/orgs/test-org/repos"

        mock_get_json.return_value = mock_repos_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value=mock_public_repos_url,
        ) as mock_url:
            client = GithubOrgClient("test-org")
            result = client.public_repos()
            expected = ["repo1", "repo2", "repo3"]

            self.assertEqual(result, expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_public_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),  # Case when 'license' is missing
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test that GithubOrgClient.has_license correctly checks for licenses.
        """
        # Create an instance of GithubOrgClient
        client = GithubOrgClient("test-org")

        # Call has_license with the repo and license_key
        result = client.has_license(repo, license_key)

        # Assert the result matches the expected value
        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos
    and public_repos with a license filter.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class by patching requests.get
        and defining the behavior for different endpoints.
        """
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Set the side effect for mocked requests.get
        def mock_get(url):
            """
            Mocked `requests.get` behavior.
            """
            class MockResponse:
                def __init__(self, json_data):
                    self._json_data = json_data

                def json(self):
                    return self._json_data

            if "orgs" in url:
                return MockResponse(org_payload)
            elif "repos" in url:
                return MockResponse(repos_payload)
            return MockResponse([])

        cls.mock_get.side_effect = mock_get

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test class by stopping the patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test that public_repos returns the expected list of repositories.
        """
        client = GithubOrgClient("test-org")
        result = client.public_repos()
        self.assertEqual(result, expected_repos)

    def test_public_repos_with_license(self):
        """
        Test that public_repos filters repositories by the apache-2.0 license.
        """
        client = GithubOrgClient("test-org")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, apache2_repos)


if __name__ == "__main__":
    unittest.main()
