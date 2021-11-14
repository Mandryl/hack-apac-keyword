from flask import Flask, jsonify,request,Blueprint,abort
from api.keyword import extract_keyword
app = Flask(__name__)
 
@app.route('/',method=["GET"])
def hello_world():

    return jsonify({'message': 'Hello world'})

@app.route('/keyword', methods=["GET"])
def get_user():
    keyword = request.args.get("inkeyword")
    keywordjson = extract_keyword(keyword)
    return jsonify(keywordjson)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8888, debug=True)