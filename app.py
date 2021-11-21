from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify, json
import os
from datetime import datetime
from database import urlall
import random
import string
DATABASENAME = "urls"
ConfigDATABASE_URL = os.environ.get("DATABASE_URL", "12345")
db = urlall(ConfigDATABASE_URL, DATABASENAME)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/shrink', methods = ['POST'])
def shrink():
    # TODO parse the input
    new_url = request.form['url_input']
    print(new_url)
    shorturl = ''.join([random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for n in range(5)])
    print(shorturl)
    # First, we check if this URL isn't already shortened
    surls = db.is_surl_exist(shorturl)
    if not surls:
        # In case it doesn't exist
        surls = db.add_url(shorturl, new_url)
        shortedurl = shorturl
    else:
        # If exists, just update the update date
        return redirect('/404')

    return redirect('/info/{shortedurl}'.format(shortedurl = shortedurl))

@app.route('/api', methods = ['GET'])
def apishrink():
    # TODO parse the input
    new_url = request.args['url']
    print(new_url)
    shorturl = ''.join([random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for n in range(5)])
    print(shorturl)
    # First, we check if this URL isn't already shortened
    surls = db.is_surl_exist(shorturl)
    if not surls:
        # In case it doesn't exist
        surls = db.add_url(shorturl, new_url)
        ase_url = request.base_url[:-3]
        shortedurl = ase_url + shorturl
        return jsonify(
            {
                "url": shortedurl
            }
        )
    else:
        # If exists, just update the update date
        return jsonify(
            {
                "error": "something went wrong"
            }
        )

@app.route('/urlinfo', methods = ['GET'])
def apishrink():
    # TODO parse the input
    new_url = request.args['url']
    print(new_url)
    #shorturl = ''.join([random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for n in range(5)])
    #print(shorturl)
    # First, we check if this URL isn't already shortened
    surls = db.is_url_exist(new_url)
    if not surls:
        url = db.get_url(new_url)
        surl = url['shurl']
        return jsonify(
            {
                "url": surl
            }
        )
    else:
        # If exists, just update the update date
        return jsonify(
            {
                "error": "something went wrong"
            }
        )

@app.route('/info/<url_hash>', methods=['POST', 'GET'])
def info(url_hash):
    _url = db.is_surl_exist(url_hash)
    if _url:
        domain = request.headers['host']
        url = db.get_info(url_hash)
        ssurl = url['shurl']
        return render_template('info.html', url = ssurl, oldurl = url['url'], domain = domain)
    else:
        return redirect('/404')

@app.route('/<url_hash>')
def page_redirect(url_hash):
    _url = db.is_surl_exist(url_hash)

    if _url:
        #_url.click_count += 1
        #db.session.commit()
        url = db.get_info(url_hash)
        urlin = url['url']
        return redirect(urlin)
    else:
        return redirect('/404')

@app.route('/404')
def not_found():
    return render_template('404.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000, use_reloader=True, threaded=True)


