from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from main import app
from hashlib import md5

db = SQLAlchemy(app)

class Url(db.Model):
    id =  db.Column('id', db.Integer, primary_key=True)
    url = db.Column('url', db.String(200))
    url_hash = db.Column('url_hash', db.String(8))
    click_count = db.Column('click_count', db.Integer)
    ip = db.Column('ip', db.String(24))
    creation_date = db.Column('creation_date', db.DateTime)
    last_access = db.Column('last_access', db.DateTime)
    update_date = db.Column('update_date', db.DateTime)

    def __init__(self, url, ip):
        url_full_hash = md5(url.encode()).hexdigest()
        url_hash = url_full_hash[:8]
        now = datetime.utcnow()

        self.url = url
        self.url_hash = url_hash
        self.click_count = 0
        self.ip = ip
        self.creation_date = now
        self.last_access = now
        self.update_date = now
