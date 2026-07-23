"""
Main blueprint: dashboard for Collection Owners.
"""

from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from bson.objectid import ObjectId

main_bp = Blueprint('main', __name__)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    db = current_app.db
    user_id = ObjectId(current_user.id)

    categories = list(db.categories.find({'user_id': user_id}).sort('name', 1))
    collections = list(db.collections.find({'user_id': user_id}).sort('name', 1))

    # Enrich collections with category name and item count
    for col in collections:
        cat = db.categories.find_one({'_id': col.get('category_id')})
        col['category_name'] = cat['name'] if cat else 'Uncategorised'
        col['item_count'] = db.items.count_documents({'collection_id': col['_id']})

    return render_template('dashboard.html',
                           categories=categories,
                           collections=collections)
