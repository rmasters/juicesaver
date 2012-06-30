from app import db

class Download(db.Model):
    __tablename__ = 'downloads'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    download_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
