"""
Collections blueprint: CRUD for categories and collections.
Implements FR-02, FR-03, FR-06 (visibility).
Includes pagination and sorting for the collection item view.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from datetime import datetime
import math

collections_bp = Blueprint('collections', __name__, url_prefix='/collections')

PER_PAGE_OPTIONS = [5, 10, 20, 100]
DEFAULT_PER_PAGE = 10


def _get_user_id():
    return ObjectId(current_user.id)


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


@collections_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if not name:
            flash('Category name is required.', 'danger')
            return render_template('collections/category_form.html')

        doc = {
            'user_id': _get_user_id(),
            'name': name,
            'description': description,
            'created_at': datetime.utcnow()
        }
        current_app.db.categories.insert_one(doc)
        flash('Category created successfully.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('collections/category_form.html')


@collections_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_collection():
    db = current_app.db
    categories = list(db.categories.find({'user_id': _get_user_id()}).sort('name', 1))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        category_id = request.form.get('category_id')
        is_public = request.form.get('is_public') == 'on'

        if not name:
            flash('Collection name is required.', 'danger')
            return render_template('collections/collection_form.html', categories=categories)

        doc = {
            'user_id': _get_user_id(),
            'category_id': ObjectId(category_id) if category_id else None,
            'name': name,
            'description': description,
            'is_public': is_public,
            'created_at': datetime.utcnow()
        }
        db.collections.insert_one(doc)
        flash('Collection created successfully.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('collections/collection_form.html', categories=categories)


@collections_bp.route('/<collection_id>')
@login_required
def view_collection(collection_id):
    db = current_app.db
    collection = db.collections.find_one({
        '_id': ObjectId(collection_id),
        'user_id': _get_user_id()
    })
    if not collection:
        flash('Collection not found or access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    page, per_page = _parse_pagination()
    sort_key = request.args.get('sort', 'name_asc')
    sort_map = {
        'name_asc': [('name', 1)],
        'name_desc': [('name', -1)],
        'newest': [('created_at', -1)],
        'oldest': [('created_at', 1)],
    }
    sort = sort_map.get(sort_key, [('name', 1)])

    query = {'collection_id': ObjectId(collection_id)}
    total = db.items.count_documents(query)
    total_pages = max(1, math.ceil(total / per_page))
    page = min(page, total_pages)
    skip = (page - 1) * per_page

    items = list(db.items.find(query).sort(sort).skip(skip).limit(per_page))

    return render_template(
        'collections/view.html',
        collection=collection,
        items=items,
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        sort=sort_key,
        per_page_options=PER_PAGE_OPTIONS,
    )


@collections_bp.route('/<collection_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_collection(collection_id):
    db = current_app.db
    collection = db.collections.find_one({
        '_id': ObjectId(collection_id),
        'user_id': _get_user_id()
    })
    if not collection:
        flash('Collection not found or access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    categories = list(db.categories.find({'user_id': _get_user_id()}).sort('name', 1))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        category_id = request.form.get('category_id')
        is_public = request.form.get('is_public') == 'on'

        if not name:
            flash('Collection name is required.', 'danger')
            return render_template('collections/collection_form.html',
                                   collection=collection, categories=categories)

        db.collections.update_one(
            {'_id': ObjectId(collection_id)},
            {'$set': {
                'name': name,
                'description': description,
                'category_id': ObjectId(category_id) if category_id else None,
                'is_public': is_public
            }}
        )
        flash('Collection updated.', 'success')
        return redirect(url_for('collections.view_collection', collection_id=collection_id))

    return render_template('collections/collection_form.html',
                           collection=collection, categories=categories)


@collections_bp.route('/<collection_id>/delete', methods=['POST'])
@login_required
def delete_collection(collection_id):
    db = current_app.db
    result = db.collections.delete_one({
        '_id': ObjectId(collection_id),
        'user_id': _get_user_id()
    })
    if result.deleted_count:
        db.items.delete_many({'collection_id': ObjectId(collection_id)})
        flash('Collection and its items deleted.', 'success')
    else:
        flash('Collection not found or access denied.', 'danger')
    return redirect(url_for('main.dashboard'))
