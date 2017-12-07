
# coding=utf-8

# Python modules
import urllib
from bs4 import BeautifulSoup

# Google App Engine Modules
from google.appengine.api import urlfetch, urlfetch_errors

# Local modules
from common import debug, html_utils, constants
from common.telegram import telegram_utils


DG_URL = "https://www.desiringgod.org/articles"

DG_DEVO_START = "<main role='main'>"
DG_DEVO_END = "</main>"

DG_DEVO_SELECT = "highlighted-section"
DG_DEVO_IGNORE = "h2"
DG_DEVO_LINKS = "href"
DG_DEVO_TITLE = "h3"

REFERENCE = "reference"
VERSION = "version"
DEVO = "devo"

def fetch_desiringgod(version="NIV"):
    formatUrl = DG_URL

    html = html_utils.fetch_html(formatUrl, DG_DEVO_START, DG_DEVO_END)
    if html is None:
        return None

    debug.log("Html: " + html)

    soup = html_utils.html_to_soup(html)

    return soup 

def get_desiringgoddevo_raw(version="NIV"):
    soup = fetch_desiringgod(version)
    if soup is None:
        return None

    for tag in soup.select(DG_DEVO_IGNORE):
        tag.decompose()

    # Steps through all the html types and mark these
    soup = html_utils.stripmd_soup(soup)

    # Finds all links and converts to markdown
    soup = html_utils.link_soup(soup, telegram_utils.link)

    # Marks the parts of the soup that we want
    soup = html_utils.mark_soup(soup, DG_DEVO_SELECT, html_utils.html_common_tags())

    # Prettifying the stuffs
    html_utils.foreach_header(soup, telegram_utils.bold)
    html_utils.style_soup(soup, html_utils.unstrip_md, html_utils.html_p_tag())
    html_utils.style_soup(soup, telegram_utils.italics, html_utils.html_p_tag())

    blocks = []
    for tag in soup(class_=DG_DEVO_SELECT):
        blocks.append(tag.text)

    passage = telegram_utils.join(blocks, "\n\n")

    return passage

def get_desiringgoddevo(version="NIV"):
    passage = get_desiringgoddevo_raw(version)

    if passage is None:
        return None

    return passage