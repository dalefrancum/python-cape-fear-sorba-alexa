import logging
import os
import re
from bs4 import BeautifulSoup
import requests
from botocore.utils import requests


logging.basicConfig(level=os.environ.get("LOGLEVEL", logging.WARN))

class CapeFearSorba(object):

    list_item_regex1 = "<li class=\"clearfix\">.*<p>([A-z .]+) .*(OPEN|CLOSED).*</li>"
    list_item_regex2 = "<li class=\"clearfix\">.*<div class=\"edn-mulitple-text-content\">\s+([A-z .]+) .*(OPEN|CLOSED).*</li>"

    @staticmethod
    def get_document_html(document_url):
        """
        Given a URL, retrieve the document and return its HTML
        :return:
        """
        r = requests.get(url=document_url)
        document_html = r.text
        return document_html

    @staticmethod
    def parse_html(html_doc):

        open_trails = []
        closed_trails = []

        soup = BeautifulSoup(html_doc, "html.parser")
        ul_element = soup.find(id="edn-effect-slider")

        for list_item in ul_element.find_all("li"):

            logging.debug(str(list_item))
            if re.search("All Trails.*OPEN", str(list_item)):
                continue

            regex = re.search(CapeFearSorba.list_item_regex1, str(list_item), re.I | re.S)

            # Second regex if the first one failed
            if not regex:
                regex = re.search(CapeFearSorba.list_item_regex2, str(list_item), re.I | re.S)

            if regex:
                trail = regex.group(1)
                if trail == "Horry Co. Bike Park":
                    trail = "Horry County Bike Park"
                status = regex.group(2)

                if status == "OPEN":
                    open_trails.append(trail)
                elif status == "CLOSED":
                    closed_trails.append(trail)
                else:
                    logging.warn("Could not determine status for trail:\nTrail: %s\nStatus: %s" % (trail, status))
            else:
                logging.warn("Could not parse list item html:\n%s" % str(list_item))

        return {"open": open_trails, "closed": closed_trails}
