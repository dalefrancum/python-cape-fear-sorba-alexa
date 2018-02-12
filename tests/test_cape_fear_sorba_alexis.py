import unittest
from mock import patch
import cfsorba_alexis.cape_fear_sorba_alexis as cape_fear_sorba_alexis


class TestCapeFearSorbaAlexis(unittest.TestCase):

    lambda_event = {}

    def test__build_output_text_all_trails_open(self):

        status_data = {
            "open": [
                "Blue Clay Bike Park",
                "Browns Creek",
                "Brunswick Nature Park",
                "Horry Co. Bike Park"
            ],
            "closed": []
        }

        alexis = cape_fear_sorba_alexis.CapeFearSorbaAlexis(self.lambda_event)
        output_text = alexis._build_output_text(status_data)

        expected_output_text = "Good news! All trails are open."
        self.assertEqual(expected_output_text, output_text)

    def test__build_output_text_all_trails_closed(self):

        status_data = {
            "open": [],
            "closed": [
                "Blue Clay Bike Park",
                "Browns Creek",
                "Brunswick Nature Park",
                "Horry Co. Bike Park"
            ]
        }

        alexis = cape_fear_sorba_alexis.CapeFearSorbaAlexis(self.lambda_event)
        expected_output_text = "Unfortunately, all trails are closed."

        output_text = alexis._build_output_text(status_data)
        self.assertEqual(expected_output_text, output_text)

    def test__build_output_text_some_open_some_close(self):

        status_data = {
            "open": [
                "Brunswick Nature Park",
                "Browns Creek",
                "Horry Co. Bike Park"
            ],
            "closed": [
                "Blue Clay Bike Park"
            ]
        }

        alexis = cape_fear_sorba_alexis.CapeFearSorbaAlexis(self.lambda_event)
        expected_output_text = "The following trails are open: %s." % ", ".join(status_data["open"])
        expected_output_text += " The following trails are closed: %s." % ", ".join(status_data["closed"])

        output_text = alexis._build_output_text(status_data)
        self.assertEqual(expected_output_text, output_text)

    @patch('cfsorba_alexis.cfsorba')
    def test_execute(self, mock_cfsorba):
        pass

    def test_lambda_handler(self):
        pass
