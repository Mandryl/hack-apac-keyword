from flask import Flask, jsonify,request,Blueprint,abort
from src.keyword_extract import extract_keyword
from src.key_article_search import extract_keyword_articlesearch
app = Flask(__name__)
 

@app.route('/api/keysearch',methods=["GET"])
def keysearch_extract_data():
    keyword = request.args.get("sentence")
    keywordjson = extract_keyword_articlesearch(keyword)
    return jsonify(keywordjson)

@app.route('/api/keyword', methods=["GET"])
def keyword_extract_data():
    keyword = request.args.get("sentence")
    keywordjson = extract_keyword(keyword)
    return jsonify(keywordjson)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)