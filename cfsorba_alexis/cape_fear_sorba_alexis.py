import logging
import os
from cfsorba import CapeFearSorba


class CapeFearSorbaAlexis(object):

    card_title = "Cape Fear Sorba Trails"

    def __init__(self, lambda_event):
        pass

    def build_speechlet_response(self, output):
        return {
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

    def build_response(session_attributes, speechlet_response):
        return {
            "version": "1.0",
            "sessionAttributes": session_attributes,
            "response": speechlet_response
        }

    def _build_output_text(self, status_data):

        open_trails = status_data["open"]
        closed_trails = status_data["closed"]

        output_text = ""

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

    def execute(self):

        cf_sorba_document_html = CapeFearSorba.get_document_html()
        cf_sorba_statuses = CapeFearSorba.parse_html(cf_sorba_document_html)

        self._build_response(status_data=cf_sorba_statuses)


def lambda_handler(lambda_event, context):
    """
    Entry point for AWS to get started.
    :param lambda_event:
    :param context:
    :return:
    """
    logging.basicConfig(level=os.environ.get("LOGLEVEL", logging.WARN))
    alexis = CapeFearSorbaAlexis(lambda_event=lambda_event)
    alexis.execute()
