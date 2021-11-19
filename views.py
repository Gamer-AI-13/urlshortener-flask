from flask import render_template, request, redirect, url_for
from main import app
import os
from datetime import datetime
from database import urlall
DATABASENAME = "urls"
ConfigDATABASE_URL = os.environ.get("DATABASE_URL", "12345")
db = urlall(ConfigDATABASE_URL, DATABASENAME)


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
        surls = db.add_url(shorturl, request.remote_addr)
        shortedurl = shorturl
    else:
        # If exists, just update the update date
        return redirect('/404')

    return redirect('/info/{shortedurl}'.format(shortedurl = shortedurl))

@app.route('/info/<url_hash>', methods=['POST', 'GET'])
def info(url_hash):
    _url = db.is_surl_exist(url_hash)
    if _url:
        domain = request.headers['host']
        url = db.get_info(url_hash)
        ssurl = url['url']
        return render_template('info.html', url = ssurl, domain = domain)
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
