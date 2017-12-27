# coding=utf-8

# Python modules
import urllib
from bs4 import BeautifulSoup

# Google App Engine Modules
from google.appengine.api import urlfetch, urlfetch_errors

# Local Modules
from common import debug, html_utils, text_utils
from common.telegram import telegram_utils
from bible import bible_utils

# Link to fetch html from
ODB_URL = "https://odb.org"

# Coarse isolation of the html block we want
ODB_START = "<article"
ODB_END = "</article>"

# Which class to isolate?
ODB_SELECT = ""
ODB_IGNORE = 


def fetch_odb():
    formatUrl = ODB_URL

    html = html_utils.fetch_html(formatUrl, ODB_START, ODB_END)
    if html is None:
        return None

    debug.log("Html: " + html)

    soup = html_utils.html_to_soup(html)

    return soup


def get_odb_raw():
    soup = fetch_odb()
    if soup is None:
        return None

    for tag in soup.select(ODB_IGNORE):
        tag.decompose()

    # Steps through all the html types and mark these
    soup = html_utils.stripmd_soup(soup)

    # Finds all links and converts to markdown
    soup = html_utils.link_soup(soup, telegram_utils.link)

    # Marks the parts of the soup that we want
    soup = html_utils.mark_soup(soup, ODB_DEVO_SELECT,
                                html_utils.html_common_tags())

    # Prettifying the stuffs
    html_utils.foreach_header(soup, telegram_utils.bold)
    html_utils.style_soup(soup, html_utils.unstrip_md, html_utils.html_p_tag())
    html_utils.style_soup(soup, telegram_utils.italics,
                          html_utils.html_p_tag())

    blocks = []
    for tag in soup(class_=ODB_DEVO_SELECT):
        blocks.append(tag.text)

    return blocks


def get_odb():
    blocks = get_odb_raw()

    if blocks is None:
        return None

    return blocks