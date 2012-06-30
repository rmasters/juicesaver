from app import db

from datetime import datetime
from dateutil import parser
from urlparse import urlparse, urlunparse

class Download(db.Model):
    __tablename__ = 'downloads'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    download_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, url=None, created_at=None, download_at=None, \
            started_at=None, completed_at=None, user=None):
        # Required attr: url
        if url:
            self.set_url(url)
        else:
            raise Exception('Required attribute url')

        # Required attr: user
        if user:
            self.set_user(user)
        else:
            raise Exception('Required attribute user')

        # Optional attr w/default: created_at
        if created_at:
            self.set_created_at(created_at)
        else:
            self.set_created_at(datetime.now())

        # Optional attrs: download_at, started_at, completed_at
        if download_at:
            self.set_download_at(download_at)
        if started_at:
            self.set_started_at(started_at)
        if completed_at:
            self.set_completed_at(completed_at)

    def set_url(self, url):
        # Check if the hostname exists in the url, if not we'll assume it's
        # invalid. Give a default scheme of http if missing.
        up = urlparse(url)
        if up.netloc == '':
            raise Exception('Malformed url given')
        if up.scheme == '':
            up.scheme = 'http'

        self.url = urlunparse(up))

    def set_created_at(self, ts):
        if type(ts) != datetime:
            ts = parser.parse(ts)
        self.created_at = ts

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
        return self.completed_at is not None \
            and self.completed_at > datetime.now()

    def is_started(self):
        return self.started_at is not None \
                and self.started_at > datetime.now()

    def status(self):
        if self.is_completed():
            return 'Completed'
        elif self.is_started():
            return 'Downloading'
        else:
            return 'Scheduled'

    """
    Return a partially abbreviated filename of the URL
    full: Return the full filename (default: false)
    """
    def filename(self, full=False):
        name = self.url.split('/')[-1]
        if not full and len(name) > 12:
            return name[0:9] + '...' + name[-3:]
        return name

    """
    Return the hostname of the URL (or None if not present)
    """
    def source(self):
        up = urlparse(self.url)
        return up.hostname

    def __repr__(self):
        return 'Download: %s from %s (%s)' % (self.filename(True), \
                self.source(), self.status())
