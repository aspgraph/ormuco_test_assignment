import json
import search_helper


# Search queries processor, storing the intermediate data
class RequestProcessor(object):
    query = ''
    keywords = []
    synonyms = []
    antonyms = []
    max_pages = 0
    max_insights = 0
    output_format = ''

    # Class constructor
    def __init__(self, query, max_pages, max_insights, output_format):
        self.query = query
        self.keywords = set([k.lower() for k in query.split(' ')])
        self.synonyms, self.antonyms = search_helper.get_synonyms_antonyms(self.keywords)
        self.max_pages = max_pages
        self.max_insights = max_insights
        self.output_format = output_format

    # Build an HTML response from the search results
    @staticmethod
    def __build_html_response(self, search_items):
        page_title = 'Search results'
        page_body = '<p><h1>%s</h1></p>' % page_title
        if search_items is None:
            return search_helper.construct_basic_html(page_title, page_body + '<p>Sorry, but nothing was found</p>')
        page_body = page_body + '<p><b>Query</b>: %s</p>' % self.query
        page_body = page_body + '<p><b>Keywords</b>: %s</p>' % ', '.join(self.keywords)
        page_body = page_body + '<p><b>Synonyms</b>: %s</p>' % \
                    (', '.join(self.synonyms) if len(self.synonyms) > 0 else 'None')
        page_body = page_body + '<p><b>Antonyms</b>: %s</p>' % \
                    (', '.join(self.antonyms) if len(self.antonyms) > 0 else 'None')
        page_body = page_body + '<p><h1>Insights</h1></p>'
        for i in range(0, min(len(search_items), self.max_pages)):
            item = search_items[i]
            url = item['link'].encode('utf-8')
            try:
                html = search_helper.load_url_content(url)
            except:
                continue
            title, insights = search_helper.extract_insights(html, self)
            if len(insights) > 0:
                text = '<p><a href="%s"><h2>%s</h2></a></p>' % (url, title)
                for j in range(0, min(len(insights), self.max_insights)):
                    start_text = '<h3>Insight %i</h3>' % (j + 1)
                    end_text = '--------------'
                    text = text + '<p>%s</p><p>%s</p><p>%s</p>' % (start_text, insights[j], end_text)
                page_body = page_body + '<div>%s</div>' % text
        return search_helper.construct_basic_html(page_title, page_body)

    # Build a JSON response from the search results
    @staticmethod
    def __build_json_response(self, search_items):
        search_results = []
        for i in range(0, min(len(search_items), self.max_pages)):
            item = search_items[i]
            url = item['link'].encode('utf-8')
            try:
                html = search_helper.load_url_content(url)
            except:
                continue
            title, insights = search_helper.extract_insights(html, self)
            if len(insights) > 0:
                cur_insights = [insights[j] for j in range(0, min(len(insights), self.max_insights))]
                search_results.append({'url': url, 'title': title, 'insights': cur_insights})

        return json.dumps({'query': self.query, 'keywords' : ', '.join(self.keywords), \
                           'synonyms' : ', '.join(self.synonyms), 'antonyms' : ', '.join(self.antonyms), \
                           'search_results': search_results})

    # Scrape Google and build a response
    @classmethod
    def get_response(cls, self):
        search_result = search_helper.load_google_search_result(self.query)
        search_items = search_result['items']
        return cls.__build_html_response(self, search_items) if self.output_format == 'html' \
            else cls.__build_json_response(self, search_items)