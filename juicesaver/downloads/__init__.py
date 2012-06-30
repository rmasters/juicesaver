from flask import Blueprint

downloads_bp = Blueprint('downloads', __name__, template_folder='templates')

import downloads.views
