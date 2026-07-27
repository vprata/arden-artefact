"""
Public blueprint: read-only gallery and search for Public Viewers.
Implements FR-06 and FR-07.
Includes pagination and sorting.
"""

from flask import Blueprint, render_template, request, current_app
from bson.objectid import ObjectId
import math

public_bp = Blueprint('public', __name__)

PER_PAGE_OPTIONS = [5, 10, 20, 100]
DEFAULT_PER_PAGE = 10


def _get_preview_images(db, collection_id, limit=4):
    """Return up to `limit` image filenames from items in this collection."""
    images = []
    items = db.items.find(
        {'collection_id': collection_id, 'images.0': {'$exists': True}},
        {'images': 1}
    ).limit(limit * 2)
    for item in items:
        for img in item.get('images', []):
            if img and img not in images:
                images.append(img)
                if len(images) >= limit:
                    return images
    return images


def _parse_pagination():
    """Read page and per_page from query string."""
    try:
        page = max(1, int(request.args.get('page', 1)))
    except ValueError:
        page = 1
    try:
        per_page = int(request.args.get('per_page', DEFAULT_PER_PAGE))
        if per_page not in PER_PAGE_OPTIONS:
            per_page = DEFAULT_PER_PAGE
    except ValueError:
        per_page = DEFAULT_PER_PAGE
    return page, per_page


def _collection_sort(sort_key):
    """Return MongoDB sort list for collections."""
    mapping = {
        'name_asc': [('name', 1)],
        'name_desc': [('name', -1)],
        'newest': [('created_at', -1)],
        'oldest': [('created_at', 1)],
    }
    return mapping.get(sort_key, [('name', 1)])


def _item_sort(sort_key):
    """Return MongoDB sort list for items."""
    mapping = {
        'name_asc': [('name', 1)],
        'name_desc': [('name', -1)],
        'newest': [('created_at', -1)],
        'oldest': [('created_at', 1)],
    }
    return mapping.get(sort_key, [('name', 1)])


@public_bp.route('/')
def index():
    """Landing page + paginated list of public collections."""
    db = current_app.db
    page, per_page = _parse_pagination()
    sort_key = request.args.get('sort', 'name_asc')
    sort = _collection_sort(sort_key)

    total = db.collections.count_documents({'is_public': True})
    total_pages = max(1, math.ceil(total / per_page))
    page = min(page, total_pages)
    skip = (page - 1) * per_page

    public_collections = list(
        db.collections.find({'is_public': True})
        .sort(sort)
        .skip(skip)
        .limit(per_page)
    )

    for col in public_collections:
        owner = db.users.find_one({'_id': col['user_id']})
        col['owner_name'] = owner['username'] if owner else 'Unknown'
        col['item_count'] = db.items.count_documents({'collection_id': col['_id']})
        col['preview_images'] = _get_preview_images(db, col['_id'], limit=4)

    return render_template(
        'public/index.html',
        collections=public_collections,
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        sort=sort_key,
        per_page_options=PER_PAGE_OPTIONS,
    )


@public_bp.route('/gallery/<collection_id>')
def gallery(collection_id):
    """Public read-only view of a single collection (paginated items)."""
    db = current_app.db
    collection = db.collections.find_one({
        '_id': ObjectId(collection_id),
        'is_public': True
    })
    if not collection:
        return render_template('public/not_found.html'), 404

    owner = db.users.find_one({'_id': collection['user_id']})
    collection['owner_name'] = owner['username'] if owner else 'Unknown'

    page, per_page = _parse_pagination()
    sort_key = request.args.get('sort', 'name_asc')
    sort = _item_sort(sort_key)

    query = {'collection_id': ObjectId(collection_id)}
    total = db.items.count_documents(query)
    total_pages = max(1, math.ceil(total / per_page))
    page = min(page, total_pages)
    skip = (page - 1) * per_page

    items = list(
        db.items.find(query).sort(sort).skip(skip).limit(per_page)
    )

    return render_template(
        'public/gallery.html',
        collection=collection,
        items=items,
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        sort=sort_key,
        per_page_options=PER_PAGE_OPTIONS,
    )


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

    from flask_login import current_user
    is_owner = current_user.is_authenticated and str(collection.get('user_id')) == current_user.id
    if not collection.get('is_public') and not is_owner:
        return render_template('public/not_found.html'), 404

    owner = db.users.find_one({'_id': collection['user_id']})
    collection['owner_name'] = owner['username'] if owner else 'Unknown'

    return render_template('public/item_detail.html', item=item, collection=collection, is_owner=is_owner)


@public_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    results = {'collections': [], 'items': []}

    if not q:
        return render_template('public/search.html', query=q, results=results)

    db = current_app.db

    try:
        results['collections'] = list(db.collections.find({
            'is_public': True,
            'name': {'$regex': q, '$options': 'i'}
        }).limit(20))

        public_cols = list(db.collections.find({'is_public': True}, {'_id': 1}))
        public_ids = [c['_id'] for c in public_cols]

        if public_ids:
            results['items'] = list(db.items.find({
                'collection_id': {'$in': public_ids},
                'name': {'$regex': q, '$options': 'i'}
            }).limit(30))

    except Exception as e:
        current_app.logger.error(f"Search error: {str(e)}")

    return render_template('public/search.html', query=q, results=results)
