from flask import render_template, request, redirect, url_for
from models import Url, db
from main import app
from datetime import datetime


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/shrink', methods = ['POST'])
def shrink():
    # TODO parse the input
    new_url = request.form['url_input']
    print(new_url)

    # First, we check if this URL isn't already shortened
    _url = Url.query.filter_by(url = new_url).first()
    if not _url:
        # In case it doesn't exist
        _url = Url(new_url, request.remote_addr)
        db.session.add(_url)
        db.session.commit()
    else:
        # If exists, just update the update date
        _url.update_date = datetime.utcnow()
        db.session.commit()

    return redirect('/info/{hash}'.format(hash = _url.url_hash))

@app.route('/info/<url_hash>', methods=['POST', 'GET'])
def info(url_hash):
    _url = Url.query.filter_by(url_hash = url_hash).first()
    if _url:
        return render_template('info.html', url = _url)
    else:
        redirect('/')

@app.route('/<url_hash>')
def page_redirect(url_hash):
    _url = Url.query.filter_by(url_hash = url_hash).first()

    if _url:
        _url.click_count += 1
        db.session.commit()
        return redirect(_url.url)
    else:
        return redirect('/404')

@app.route('/404')
def not_found():
    return render_template('404.html')
