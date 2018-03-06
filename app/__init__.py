# Import flask and libs
from flask import Flask, render_template
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
# Configurations
app.config.from_object('config')
# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
# HTTP 404
# HTTP error handling
@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

from app.controllers import app_controller as app_controller_module

# Register blueprint(s)
app.register_blueprint(app_controller_module)
