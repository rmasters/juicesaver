from main import main_bp
from flask import render_template

from models import db, Download

@main_bp.route('/')
def dashboard():

    recent_added = db.session.query(Download) \
            .filter(Download.started_at == None) \
            .order_by(Download.created_at.desc()) \
            .limit(5).all()

    return render_template('dashboard.html', queued=recent_added)
