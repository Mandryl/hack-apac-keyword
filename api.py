from flask import Flask, jsonify,request,Blueprint,abort
from src.keyword_extract import extract_keyword
from src.key_article_search import extract_keyword_articlesearch
from flask_cors import CORS,cross_origin
app = Flask(__name__)
 
CORS(app, support_credentials=True)

@app.route('/api/keysearch',method=["GET"])
def hello_world():
    keyword = request.args.get("sentence")
    keywordjson = extract_keyword_articlesearch(keyword)
    return jsonify(keywordjson)

@app.route('/api/keyword', methods=["GET","POST"])
def get_user():
    keyword = request.args.get("sentence")
    keywordjson = extract_keyword(keyword)
    return jsonify(keywordjson)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)