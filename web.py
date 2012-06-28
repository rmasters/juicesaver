from datetime import datetime, timedelta
from dateutil import parser
from functools import wraps

import random, string
from urlparse import urlparse

from flask import Flask, request, Response, session, render_template, redirect, url_for, make_response
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

"""
A queued/finished download

"""
class Download(db.Model):
    __tablename__ = 'downloads'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    created_at = db.Column(db.DateTime)
    download_at = db.Column(db.DateTime, nullable=True)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, url=None, created_at=None, download_at=None, started_at=None, completed_at=None, user=None):
        if url:
            self.url = url

        if created_at:
            self.set_created_at(created_at)
        else:
            self.created_at = datetime.now()

        if download_at:
            self.set_download_at(download_at)
        if started_at:
            self.set_started_at(started_at)
        if completed_at:
            self.set_completed_at(completed_at)

        if user:
            self.set_user(user)

    def set_user(self, user):
        if type(user) == User:
            user = user.id
        self.user = int(user)

    def set_download_at(self, ts):
        if type(ts) != datetime:
            ts = parser.parse(ts)
        self.download_at = ts

    def set_started_at(self, ts):
        if type(ts) != datetime:
            ts = parser.parse(ts)
        self.started_at = ts

    def set_completed_at(self, ts):
        if type(ts) != datetime:
            ts = parser.parse(ts)
        self.completed_at = ts

    def is_completed(self):
        return self.completed_at is not None

    def is_started(self):
        return self.started_at is not None

    def status(self):
        if self.is_completed():
            return 'Completed'
        elif self.is_started():
            return 'Downloading'
        else:
            return 'Scheduled'

    def filename(self):
        fn = self.url.split('/')[-1]
        if len(fn) > 10:
            return fn[0:9] + '...' + fn[-3:]
        return fn

    def source(self):
        up = urlparse(self.url)
        return up.hostname

"""
User

"""
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    password = db.Column(db.String())
    created_at = db.Column(db.DateTime)
    authorised_at = db.Column(db.DateTime, nullable=True)
    session_token = db.Column(db.Text, nullable=True)

    downloads = db.relationship('Download', backref='created_by', lazy='dynamic')

    def __init__(self, name=None, password=None, created_at=None, authorised_at=None):
        if name:
            self.name = name
        if password:
            self.password = password
        if created_at:
            self.created_at = created_at
        if authorised_at:
            self.authorised_at = authorised_at

    def is_authorised(self):
        return self.authorised_at is None

    def create_token(self):
        alpha = string.ascii_letters + string.digits
        token = ''
        for i in range(0, 64):
            token += alpha[random.randint(0, len(alpha)-1)]
        self.session_token = token

try:
    tables_before = db.engine.table_names()
    db.create_all()
    # If this is the first run, create the admin user
    if len(tables_before) == 0 and len(db.engine.table_names()) > 0:
        admin = User(name='admin', password='admin', \
            created_at=datetime.now(), authorised_at=datetime.now())
        db.session.add(admin)
        db.session.commit()
except Exception as e:
    print e

"""
Helper method to check authorisation

"""
active_user = None
def is_authenticated():
    if 'user' not in request.cookies:
        return False

    global active_user

    try:
        cookie = request.cookies.get('user')
        cookie_bits = cookie.split('&')
        cred = {}
        for k, v in [c.split('=') for c in cookie_bits]:
            cred[k] = v

        u = db.session.query(User) \
            .filter(User.id == cred['id']) \
            .filter(User.session_token == cred['token']) \
            .one()
        active_user = u
    except Exception as e:
        print e, type(e)
        return False

    return True

def requires_authentication(func):
    @wraps(func)
    def _auth_decorator(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return _auth_decorator

@app.route('/')
@requires_authentication
def home():
    # Dashboard

    recently_queued = db.session.query(Download).filter(Download.started_at == None).order_by(Download.created_at.desc()).limit(5).all()

    recently_downloaded = db.session.query(Download).filter(Download.completed_at != None).order_by(Download.completed_at.desc()).limit(5).all()

    next_to_download = db.session.query(Download).filter(Download.completed_at == None).order_by(Download.download_at.asc()).all()

    return render_template('home.html', user=active_user, queued=recently_queued, finished=recently_downloaded, next=next_to_download)

@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = []
    if 'name' in request.form and 'password' in request.form:
        try:
            u = db.session.query(User) \
                    .filter(User.name == request.form['name']) \
                    .filter(User.password == request.form['password']) \
                    .one()

            u.create_token()
            db.session.add(u)
            db.session.commit()

            resp = make_response(render_template('logged_in.html'))

            cookie_str = 'id=%d&token=%s' % (u.id, u.session_token)
            expiry_dt = datetime.now() + timedelta(days=1)

            resp.set_cookie('user', cookie_str, expires=expiry_dt)
            return resp
        except Exception as e:
            errors.append("Invalid credentials")
            errors.append(e)
    return render_template('login.html', errors=errors)

@app.route('/logout')
@requires_authentication
def logout():
    resp = make_response(render_template('logged_out.html'))
    resp.set_cookie('user', value='', expires=-1)

    return resp

@app.route('/register')
def register():
    pass

@app.route('/queue')
@requires_authentication
def queue():
    downloads = db.session.query(Download).order_by(Download.created_at.desc()).all()
    return render_template('queue.html', downloads=downloads, user=active_user)

@app.route('/schedule', methods=['GET', 'POST'])
@requires_authentication
def schedule():
    errors = []
    if request.form:
        d = Download(url=request.form['url'], 
                download_at=request.form['download_at'],
                user=active_user)
        db.session.add(d)
        db.session.commit()

        return redirect(url_for('queue'))

    return render_template('schedule.html', errors=errors, user=active_user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
