"""
Main blueprint: dashboard for Collection Owners.
Includes pagination and sorting.
"""

from flask import Blueprint, render_template, request, current_app
from flask_login import login_required, current_user
from bson.objectid import ObjectId
import math

main_bp = Blueprint('main', __name__)

PER_PAGE_OPTIONS = [5, 10, 20, 100]
DEFAULT_PER_PAGE = 10


def _get_preview_images(db, collection_id, limit=4):
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


@main_bp.route('/dashboard')
@login_required
def dashboard():
    db = current_app.db
    user_id = ObjectId(current_user.id)

    page, per_page = _parse_pagination()
    sort_key = request.args.get('sort', 'name_asc')
    sort_map = {
        'name_asc': [('name', 1)],
        'name_desc': [('name', -1)],
        'newest': [('created_at', -1)],
        'oldest': [('created_at', 1)],
    }
    sort = sort_map.get(sort_key, [('name', 1)])

    categories = list(db.categories.find({'user_id': user_id}).sort('name', 1))

    query = {'user_id': user_id}
    total = db.collections.count_documents(query)
    total_pages = max(1, math.ceil(total / per_page))
    page = min(page, total_pages)
    skip = (page - 1) * per_page

    collections = list(
        db.collections.find(query).sort(sort).skip(skip).limit(per_page)
    )

    for col in collections:
        cat = db.categories.find_one({'_id': col.get('category_id')})
        col['category_name'] = cat['name'] if cat else 'Uncategorised'
        col['item_count'] = db.items.count_documents({'collection_id': col['_id']})
        col['preview_images'] = _get_preview_images(db, col['_id'], limit=4)

    return render_template(
        'dashboard.html',
        categories=categories,
        collections=collections,
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        sort=sort_key,
        per_page_options=PER_PAGE_OPTIONS,
    )
