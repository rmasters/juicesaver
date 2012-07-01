from downloads import downloads_bp
from flask import render_template

@downloads_bp.route('/')
def list_downloads():
    return render_template('list_downloads.html')
