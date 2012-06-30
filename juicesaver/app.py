from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from main import main_bp
from users import users_bp
from downloads import downloads_bp

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(downloads_bp, url_prefix='/downloads')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
