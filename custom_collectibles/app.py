"""
Custom Collectibles - Main Application Entry Point
A web-based collection management system with dynamic custom fields.
"""

from flask import Flask, flash, redirect, request, url_for
from flask_login import LoginManager
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.exceptions import RequestEntityTooLarge
from config import Config
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # MongoDB connection
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client.get_default_database()

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    from blueprints.auth import User

    @login_manager.user_loader
    def load_user(user_id):
        user_data = app.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

    # ------------------------------------------------------------------
    # Friendly error handling for common situations
    # ------------------------------------------------------------------
    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        """Show a clear message instead of a generic 413 page."""
        max_mb = app.config.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024) // (1024 * 1024)
        flash(
            f'The file you tried to upload is too large. '
            f'Maximum allowed size is {max_mb} MB. Please choose a smaller image.',
            'danger'
        )
        # Try to send the user back to the form they came from
        referrer = request.referrer
        if referrer:
            return redirect(referrer)
        return redirect(url_for('main.dashboard'))

    @app.errorhandler(413)
    def handle_413(e):
        return handle_file_too_large(e)

    # Register blueprints
    from blueprints.auth import auth_bp
    from blueprints.main import main_bp
    from blueprints.collections import collections_bp
    from blueprints.items import items_bp
    from blueprints.public import public_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(collections_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(public_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
