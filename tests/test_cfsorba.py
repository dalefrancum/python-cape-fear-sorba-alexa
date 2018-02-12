import unittest
from mock import Mock, patch
import cfsorba_alexis.cfsorba as cfsorba


class TestCapeFearSorba(unittest.TestCase):

    @patch('cfsorba_alexis.cfsorba.requests')
    def test_get_document_html(self, mock_requests):
        test_html = "<html></html>"
        mock_requests.get.return_value = Mock(status_code=200, text=test_html)
        document_html = cfsorba.CapeFearSorba.get_document_html(document_url="http://capefearsorba.org/")
        self.assertEqual(test_html, document_html)

    def test_parse_html(self):

        test_html_file = "tests/data/cfsorba_home.20170211.html"
        with file(test_html_file) as f:
            test_html = f.read()

        response = cfsorba.CapeFearSorba.parse_html(html_doc=test_html)

        expected_response = {
            "open": [
                "Brunswick Nature Park",
                "Browns Creek",
                "Horry Co. Bike Park"
            ],
            "closed": [
                "Blue Clay Bike Park"
            ]
        }
        self.assertDictEqual(expected_response, response)
