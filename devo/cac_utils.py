
# Python modules
import urllib
from bs4 import BeautifulSoup

# Google App Engine Modules
from google.appengine.api import urlfetch, urlfetch_errors
from google.appengine.ext import db

# Local modules
from common import debug, html_utils, constants
from common.telegram import telegram_utils


CAC_URL = 'https://cac.org/category/daily-meditations/'

BGW_PASSAGE_CLASS = 'passage-text'
BGW_PASSAGE_START = '<div class="{}">'.format(BGW_PASSAGE_CLASS)
BGW_PASSAGE_END = '<!--END .{}-->'.format(BGW_PASSAGE_CLASS)
BGW_PASSAGE_SELECT = 'bgw-passage-text'
BGW_PASSAGE_IGNORE = '.passage-display, .footnote, .footnotes, .crossrefs, .publisher-info-bottom'
BGW_PASSAGE_TITLE = '.passage-display-bcv'

REFERENCE = 'reference'
VERSION = 'version'
PASSAGE = 'passage'

def extract_devo(html):
    return html_utils.sub_html(html, BGW_PASSAGE_START, BGW_PASSAGE_END)

def fetch_cac(query, version='NIV'):
    formatRef = urllib.quote(query.lower().strip())
    formatUrl = CAC_URL

    try:
        debug.log('Attempting to fetch: ' + formatUrl)
        result = urlfetch.fetch(formatUrl, deadline=constants.URL_TIMEOUT)
    except urlfetch_errors.Error as e:
        debug.log('Error fetching: ' + str(e))
        return None

    # Format using BS4 into a form we can use for extraction
    passageHtml = extract_devo(result.content)
    if passageHtml is None:
        return None

    soup = BeautifulSoup(passageHtml, 'lxml').select_one('.{}'.format(BGW_PASSAGE_CLASS))
    
    debug.log("Soup has been made")

    return soup 

def get_passage_raw(ref, version='NIV'):
    debug.log('Querying for passage ' + ref)

    passageSoup = fetch_bgw(ref, version)
    if passageSoup is None:
        return None

    # Prepare the title and header
    passageReference = passage_soup.select_one(BGW_PASSAGE_TITLE).text.strip()
    passageVersion = version

    # Remove the unnecessary tags
    for tag in passageSoup.select(BGW_PASSAGE_IGNORE):
        tag.decompose()

    # Steps through all the html types and mark these
    soup = html_utils.stripmd_soup(passageSoup)
    soup = html_utils.mark_soup(passageSoup, 
    BGW_PASSAGE_SELECT,
    html_utils.HTML_HEADER_TAGS + html_utils.HTML_TEXT_TAGS)

    html_utils.foreach_header(passageSoup, telegram_utils.bold)

    # Special formatting for chapter and verse
    for tag in soup.select('.chapternum'):
        tag.string = telegram_utils.bold(tag.text)
    for tag in soup.select('.versenum'):
        tag.string = telegram_utils.italics(html_utils.to_sup(tag.text))

    # Only at the last step do we do other destructive formatting
    soup = html_utils.strip_soup(passageSoup)

    passageBlocks = []
    for tag in soup(class_=BGW_PASSAGE_SELECT):
        passageBlocks.append(tag.text)

    passageText = telegram_utils.join(passageBlocks, '\n\n')

    debug.log("Finished parsing soup")

    return BGWPassage(passageReference, passageVersion, passageText)

def get_passage(ref, version='NIV'):
    passage = get_passage_raw(ref, version)

    if passage is None:
        return None

    passageFormat = telegram_utils.bold(passage.get_reference())
    passageFormat += ' ' + telegram_utils.bracket(passage.get_version())
    passageFormat += '\n\n' + passage.get_text()

    return passageFormat

def get_reference(query):
    debug.log('Querying for reference ' + query)

    passageSoup = fetch_bgw(query)
    if passageSoup is None:
        return None

    reference = passageSoup.select_one(BGW_PASSAGE_TITLE).text
    reference = reference.strip()

    return reference