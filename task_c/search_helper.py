import re
import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet
from googleapiclient.discovery import build
import config


# Load all URL content (likely HTML) from a resource
def load_url_content(url, par=None):
    user_agent = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
    if par is not None:
        response = requests.get(url, headers=user_agent, params=par)
    else:
        response = requests.get(url, headers=user_agent)
    return response.text


# Get all synonyms and antonyms of the input keywords
def get_synonyms_antonyms(keywords):
    lemmas = []
    synonyms = []
    antonyms = []
    for kw in keywords:
        for syn in wordnet.synsets(kw.encode('utf-8')):
            cur_lemmas = syn.lemmas()
            lemmas.extend(cur_lemmas)
            synonyms.extend([l.name() for l in cur_lemmas])
            antonyms.extend([a.name() for a in l.antonyms() for l in cur_lemmas])

    synonyms = set([s.lower() for s in synonyms if s.find('_') == -1]) - keywords
    antonyms = set([a.lower() for a in antonyms if a.find('_') == -1]) - keywords - synonyms
    return synonyms, antonyms


# Give a rating to a text paragraph
# Rating considers the length of the paragraph, amount of matching keywords,
# their synonyms and antonyms.
def __rate_paragraph(words, processor, num_links):
    word_count = len(words)
    word_rating = len(words.intersection(processor.keywords))
    syn_rating = len(words.intersection(processor.synonyms))
    ant_rating = len(words.intersection(processor.antonyms))

    # a neural network could be trained here to get optimal weights,
    # but to keep it simple, let's predefine these
    # 5 synonyms beat an extra keyword, 2 antonyms beat a synonym
    relevance_rating = word_rating + syn_rating*0.11 + ant_rating*0.056
    if relevance_rating == 0 or word_count < 5:
        return 0.0

    # let's predefine 99 or 100 to be an optimal number of words in an insight
    count_rating = abs(1.0 / (word_count - 99.5))
    return count_rating + relevance_rating - num_links/2.0


# Extract paragraphs from a BeautifulSoup HTML block
def __extract_paragraphs(div_soup, processor):
    # Let's define paragraphs as pieces of text inside a div or a p HTML block
    tags = div_soup.find_all(['div', 'p'])
    filtered_tags = []
    for tag in tags:
        # Let's don't include higher-level blocks, as these contain sub-paragraphs
        sub_div = tag.find(['div', 'p'])
        if sub_div is None:
            filtered_tags.append(tag)
    tags = filtered_tags
    # Filtering and sorting paragraphs by their word count and relevance
    filtered_tags = []
    for tag in tags:
        text = tag.get_text()
        num_links = len(tag.find_all('a'))
        if text == u'':
            continue
        words = set([w.lower() for w in re.findall(r'\w+', text)])
        rating = __rate_paragraph(words, processor, num_links)
        if rating > 0:
            filtered_tags.append((rating, tag))
    filtered_tags.sort(reverse=True)
    return [unicode(t[1]) for t in filtered_tags]


# Extract all insights from an HTML
def extract_insights(html, processor):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('head').find('title').string
    insights = __extract_paragraphs(soup.find('body'), processor)
    return title, [insight.strip() for insight in insights]


# Run Google Custom Search and get the results
def load_google_search_result(query):
    service = build('customsearch', 'v1', developerKey=config.api_key)
    res = service.cse().list(q=query, cx=config.cse_id).execute()
    return res


# Construct basic HTML-format text out of page title and body
def construct_basic_html(title, body):
    return '<html><head><title>%s</title></head><body>%s</body></html> ' % (title, body)