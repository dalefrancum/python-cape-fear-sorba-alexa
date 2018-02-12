import unittest
from mock import patch
import cfsorba_alexa.cape_fear_sorba_alexa as cape_fear_sorba_alexa


class TestCapeFearSorbaAlexa(unittest.TestCase):

    lambda_event = {}

    def test_build_output_text_all_trails_open(self):

        status_data = {
            "open": [
                "Blue Clay Bike Park",
                "Browns Creek",
                "Brunswick Nature Park",
                "Horry Co. Bike Park"
            ],
            "closed": []
        }

        alexa = cape_fear_sorba_alexa.CapeFearSorbaAlexa(self.lambda_event)
        output_text = alexa._build_output_text(status_data)

        expected_output_text = "Good news! All trails are open."
        self.assertEqual(expected_output_text, output_text)

    def test_build_output_text_all_trails_closed(self):

        status_data = {
            "open": [],
            "closed": [
                "Blue Clay Bike Park",
                "Browns Creek",
                "Brunswick Nature Park",
                "Horry Co. Bike Park"
            ]
        }

        alexa = cape_fear_sorba_alexa.CapeFearSorbaAlexa(self.lambda_event)
        expected_output_text = "Unfortunately, all trails are closed."

        output_text = alexa._build_output_text(status_data)
        self.assertEqual(expected_output_text, output_text)

    def test_build_output_text_some_open_some_close(self):

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

        alexa = cape_fear_sorba_alexa.CapeFearSorbaAlexa(self.lambda_event)
        expected_output_text = "The following trails are open: %s." % ", ".join(status_data["open"])
        expected_output_text += " The following trails are closed: %s." % ", ".join(status_data["closed"])

        output_text = alexa._build_output_text(status_data)
        self.assertEqual(expected_output_text, output_text)

    def test_build_output_text_could_not_be_determined(self):

        status_data = {
            "open": [],
            "closed": []
        }

        alexa = cape_fear_sorba_alexa.CapeFearSorbaAlexa(self.lambda_event)
        expected_output_text = "I'm sorry, trail statuses could not be determined."

        output_text = alexa._build_output_text(status_data)
        self.assertEqual(expected_output_text, output_text)

    def test_build_response(self):

        test_output = "Good news! All trails are open."

        alexa = cape_fear_sorba_alexa.CapeFearSorbaAlexa(self.lambda_event)
        response = alexa._build_response(output=test_output)

        expected_response = {
            "version": "1.0",
            "sessionAttributes": {},
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": test_output
                },
                "card": {
                    "type": "Simple",
                    "title": "Cape Fear Sorba Trails",
                    "content": test_output
                },
                "shouldEndSession": True
            }
        }
        self.assertDictEqual(expected_response, response)

    @patch('cfsorba_alexa.cape_fear_sorba_alexa.CapeFearSorba')
    @patch('cfsorba_alexa.cape_fear_sorba_alexa.CapeFearSorbaAlexa._build_output_text')
    @patch('cfsorba_alexa.cape_fear_sorba_alexa.CapeFearSorbaAlexa._build_response')
    def test_execute(self, mock_build_response, mock_build_output_text, mock_cfsorba):

        mock_status_data = {
            "open": [
                "Blue Clay Bike Park",
                "Browns Creek",
                "Brunswick Nature Park",
                "Horry Co. Bike Park"
            ],
            "closed": []
        }

        mock_cfsorba.get_document_html.return_value = "<html></html>"
        mock_cfsorba.parse_html.return_value = mock_status_data
        mock_build_output_text.return_value = "Good news! All trails are open."

        alexa = cape_fear_sorba_alexa.CapeFearSorbaAlexa(self.lambda_event)
        alexa.execute()

        mock_cfsorba.get_document_html.assert_called()
        mock_cfsorba.parse_html.assert_called_with(html_doc="<html></html>")
        mock_build_output_text.assert_called_with(status_data=mock_status_data)
        mock_build_response.assert_called_with(output="Good news! All trails are open.")

    def test_lambda_handler(self):
        pass
