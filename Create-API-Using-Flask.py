
import flask
from flask import request, jsonify


#creating ka Flask App
app =flask.Flask(__name__)

phone = [
    {'id':0,
     'name':'Samsung'},
    {'id':1,'name':'iphone'}
    ]


#Home route
@app.route('/', methods=['GET'])
def home():
    return "<h1>First App<h1>"


@app.route('/phone/',methods=['GET'])
def api():
    return jsonify(phone)


@app.route('/phone/<id>',methods=['GET'])
def api_id(id):
    return jsonify(phone[int(id)])

if __name__=='__main__':
    app.run(debug=True)
        