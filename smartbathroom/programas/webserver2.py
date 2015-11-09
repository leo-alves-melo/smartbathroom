
import os.path
from functools import wraps
from flask import Flask, url_for, jsonify, redirect, request, current_app, send_from_directory
from TwitterAPI import TwitterAPI

# TWITTER ACCOUNT DATA
CONSUMER_KEY = '' #Insert here your consumer key
CONSUMER_SECRET = '' #Insert here your consumer secret
ACCESS_TOKEN_KEY = '' #Insert here your token key
ACCESS_TOKEN_SECRET = '' #Insert here your token secret

api = TwitterAPI(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)

app = Flask(__name__)

def support_jsonp(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
                callback = request.args.get('callback', False)
                if callback:
                        content = str(callback) + '(' + str(f(*args,**kwargs).data) + ')'
                        return current_app.response_class(content,mimetype='application/javascript')
                else:
                        return f(*args, **kwargs)
        return decorated_function

@app.route('/usound')
@support_jsonp
def usoundinfo():
        f = open('usound', 'r')
        distance = int(float(f.readline()))
        f.close()
        distJson = {"usound":distance}
        resp = jsonify(distJson)
        resp.status_code = 200
        return resp

@app.route('/peopleInside')
@support_jsonp
def peopleinfo():
        f = open('currnum', 'r')
        pessoas = int(f.readline())
        f.close()
        pessoasJson = {"peopleInside":pessoas}
        resp = jsonify(pessoasJson)
        resp.status_code = 200
        return resp

@app.route('/maxInside')
@support_jsonp
def maxinfo():
        f = open('maxnum', 'r')
        max = int(f.readline())
        f.close()
        maxJson = {"maxInside":max}
        resp = jsonify(maxJson)
        resp.status_code = 200
        return resp

@app.route('/totalInside')
@support_jsonp
def totalinfo():
        f = open('totalnum', 'r')
        total = int(f.readline())
        f.close()
        if(total > 5):
                text = 'Ja entraram '+str(total)+' pessoas nesse banheiro. Venha me limpar!'
                tweet = api.request('statuses/update', {'status': text})
        totalJson = {"totalInside":total}
        resp = jsonify(totalJson)
        resp.status_code = 200
        return resp


if __name__ == '__main__':
        app.run(debug=True, host="10.94.1.32", port=80)
