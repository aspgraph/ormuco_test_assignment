from flask import Flask
from flask import request
import nltk
import search_helper
import search_model

# API web engine powered by Flask
app = Flask(__name__)


# Root directory
@app.route('/', methods=['GET'])
def root():
    return search_helper.construct_basic_html('Hi!', '<p>Hi! To use this api, please use /search?query={your_query}</p>')


# Search request processing
@app.route('/search', methods=['GET'])
def search():
    if 'query' in request.args:
        query = request.args.get('query')
        max_pages = int(request.args.get('max_pages')) if 'max_pages' in request.args else 5
        max_insights = int(request.args.get('max_insights')) if 'max_insights' in request.args else 5
        output_format = request.args.get('output_format') if 'output_format' in request.args else 'html'
        processor = search_model.RequestProcessor(query, max_pages, max_insights, output_format)
        return search_model.RequestProcessor.get_response(processor)
    else:
        return search_helper.construct_basic_html('Error!', 'Error! Please add the "query" argument to your query.')


# Program entry point
if __name__ == '__main__':
    nltk.download('wordnet')
    app.run(debug=True)
