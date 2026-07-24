"""
Public blueprint: read-only gallery and search for Public Viewers.
Implements FR-06 and FR-07.
"""

from flask import Blueprint, render_template, request, current_app
from bson.objectid import ObjectId

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    """Landing page + list of public collections."""
    db = current_app.db
    public_collections = list(
        db.collections.find({'is_public': True}).sort('name', 1).limit(50)
    )
    # Enrich with owner username and item count
    for col in public_collections:
        owner = db.users.find_one({'_id': col['user_id']})
        col['owner_name'] = owner['username'] if owner else 'Unknown'
        col['item_count'] = db.items.count_documents({'collection_id': col['_id']})

    return render_template('public/index.html', collections=public_collections)


@public_bp.route('/gallery/<collection_id>')
def gallery(collection_id):
    """Public read-only view of a single collection."""
    db = current_app.db
    collection = db.collections.find_one({
        '_id': ObjectId(collection_id),
        'is_public': True
    })
    if not collection:
        return render_template('public/not_found.html'), 404

    owner = db.users.find_one({'_id': collection['user_id']})
    collection['owner_name'] = owner['username'] if owner else 'Unknown'

    items = list(db.items.find({'collection_id': ObjectId(collection_id)}).sort('name', 1))
    return render_template('public/gallery.html', collection=collection, items=items)


@public_bp.route('/item/<item_id>')
def item_detail(item_id):
    """Public (or owner) single item detail page – full image + all fields."""
    db = current_app.db
    try:
        item = db.items.find_one({'_id': ObjectId(item_id)})
    except Exception:
        return render_template('public/not_found.html'), 404

    if not item:
        return render_template('public/not_found.html'), 404

    collection = db.collections.find_one({'_id': item['collection_id']})
    if not collection:
        return render_template('public/not_found.html'), 404

    # Only allow viewing if the collection is public OR the current user owns it
    from flask_login import current_user
    is_owner = current_user.is_authenticated and str(collection.get('user_id')) == current_user.id
    if not collection.get('is_public') and not is_owner:
        return render_template('public/not_found.html'), 404

    owner = db.users.find_one({'_id': collection['user_id']})
    collection['owner_name'] = owner['username'] if owner else 'Unknown'

    return render_template('public/item_detail.html', item=item, collection=collection, is_owner=is_owner)


@public_bp.route('/search')
def search():
    """Simple search across public collections and their items."""
    q = request.args.get('q', '').strip()
    results = {'collections': [], 'items': []}

    if q and len(q) >= 1:
        db = current_app.db
        try:
            # Escape special regex characters
            import re
            safe_q = re.escape(q)
            regex_query = {'$regex': safe_q, '$options': 'i'}

            # Search public collections by name
            results['collections'] = list(
                db.collections.find(
                    {'is_public': True, 'name': regex_query}
                ).limit(20)
            )

            # Get IDs of public collections
            public_ids = [c['_id'] for c in db.collections.find(
                {'is_public': True}, {'_id': 1}
            )]

            if public_ids:
                results['items'] = list(
                    db.items.find({
                        'collection_id': {'$in': public_ids},
                        '$or': [
                            {'name': regex_query},
                            {'custom_fields.value': regex_query}
                        ]
                    }).limit(30)
                )
        except Exception as e:
            # Log the error but don't crash the page
            current_app.logger.error(f"Search error: {e}")
            results = {'collections': [], 'items': []}

    return render_template('public/search.html', query=q, results=results)
