import logging
import os
from cfsorba import CapeFearSorba


logging.basicConfig(level=os.environ.get("LOGLEVEL", logging.WARN))

class CapeFearSorbaAlexa(object):

    document_url = os.environ.get("CFSORBA_DOCUMENT_URL", "http://capefearsorba.org")
    speech_response_version = "1.0"
    card_title = "Cape Fear Sorba Trails"
    session_attributes = {}

    def __init__(self, lambda_event):
        pass

    def _build_output_text(self, status_data):

        open_trails = status_data["open"]
        closed_trails = status_data["closed"]

        # All trails open
        if len(open_trails) > 0 and len(closed_trails) == 0:
            output_text = "Good news! All trails are open."

        # All trails closed
        elif len(open_trails) == 0 and len(closed_trails) > 0:
            output_text = "Unfortunately, all trails are closed."

        # Some trails open, some trails closed
        elif len(open_trails) > 0 and len(closed_trails) > 0:
            output_text = "The following trails are open: %s." % ", ".join(open_trails)
            output_text += " The following trails are closed: %s." % ", ".join(closed_trails)

        # Otherwise, something went wrong retrieving the data
        else:
            output_text = "I'm sorry, trail statuses could not be determined."

        return output_text

    def _build_response(self, output):

        response = {
            "version": self.speech_response_version,
            "sessionAttributes": self.session_attributes,
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": output
                },
                "card": {
                    "type": "Simple",
                    "title": self.card_title,
                    "content": output
                },
                "shouldEndSession": True
            }
        }
        return response

    def execute(self):

        # Get the statuses from the Cape Fear SORBA site
        cf_sorba_document_html = CapeFearSorba.get_document_html(document_url=self.document_url)
        cf_sorba_statuses = CapeFearSorba.parse_html(html_doc=cf_sorba_document_html)

        # Build the response and return that
        output_text = self._build_output_text(status_data=cf_sorba_statuses)
        response = self._build_response(output=output_text)
        logging.debug(response)
        return response


def lambda_handler(lambda_event, context):
    """
    Entry point for AWS to get started.
    :param lambda_event:
    :param context:
    :return:
    """
    logging.basicConfig(level=os.environ.get("LOGLEVEL", logging.WARN))
    alexa = CapeFearSorbaAlexa(lambda_event=lambda_event)
    alexa.execute()
