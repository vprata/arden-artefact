"""
Items blueprint: CRUD for items with dynamic custom fields.
Implements FR-04 and FR-05 – the core innovation of the project.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from PIL import Image

items_bp = Blueprint('items', __name__, url_prefix='/items')


def _get_user_id():
    return ObjectId(current_user.id)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def parse_custom_fields(form):
    """
    Extract dynamic custom fields from the submitted form.
    Expected form keys: field_name_0, field_type_0, field_value_0, ...
    """
    custom_fields = []
    i = 0
    while True:
        name_key = f'field_name_{i}'
        type_key = f'field_type_{i}'
        value_key = f'field_value_{i}'

        if name_key not in form:
            break

        field_name = form.get(name_key, '').strip()
        field_type = form.get(type_key, 'text').strip()
        field_value = form.get(value_key, '').strip()

        if field_name:  # only keep fields that have a name
            # Basic type coercion
            if field_type == 'number':
                try:
                    field_value = float(field_value) if '.' in field_value else int(field_value)
                except ValueError:
                    field_value = field_value  # keep as string if conversion fails
            elif field_type == 'boolean':
                field_value = field_value.lower() in ('true', '1', 'yes', 'on')

            custom_fields.append({
                'field_name': field_name,
                'field_type': field_type,
                'value': field_value
            })
        i += 1
    return custom_fields


@items_bp.route('/new/<collection_id>', methods=['GET', 'POST'])
@login_required
def new_item(collection_id):
    db = current_app.db
    collection = db.collections.find_one({
        '_id': ObjectId(collection_id),
        'user_id': _get_user_id()
    })
    if not collection:
        flash('Collection not found or access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('Item name is required.', 'danger')
            return render_template('items/item_form.html', collection=collection)

        custom_fields = parse_custom_fields(request.form)

        # Handle image upload
        images = []
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Make unique
                unique_name = f"{ObjectId()}_{filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
                file.save(filepath)

                # Optional resize
                try:
                    with Image.open(filepath) as img:
                        img.thumbnail((800, 800))
                        img.save(filepath)
                except Exception:
                    pass  # keep original if resize fails

                images.append(unique_name)

        item_doc = {
            'collection_id': ObjectId(collection_id),
            'user_id': _get_user_id(),
            'name': name,
            'custom_fields': custom_fields,
            'images': images,
            'created_at': datetime.utcnow()
        }
        db.items.insert_one(item_doc)
        flash('Item created successfully.', 'success')
        return redirect(url_for('collections.view_collection', collection_id=collection_id))

    return render_template('items/item_form.html', collection=collection)


@items_bp.route('/<item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    db = current_app.db
    item = db.items.find_one({
        '_id': ObjectId(item_id),
        'user_id': _get_user_id()
    })
    if not item:
        flash('Item not found or access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    collection = db.collections.find_one({'_id': item['collection_id']})

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('Item name is required.', 'danger')
            return render_template('items/item_form.html', collection=collection, item=item)

        custom_fields = parse_custom_fields(request.form)

        update = {
            'name': name,
            'custom_fields': custom_fields
        }

        # Optional new image
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_name = f"{ObjectId()}_{filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
                file.save(filepath)
                try:
                    with Image.open(filepath) as img:
                        img.thumbnail((800, 800))
                        img.save(filepath)
                except Exception:
                    pass
                update['images'] = [unique_name]  # replace existing image

        db.items.update_one({'_id': ObjectId(item_id)}, {'$set': update})
        flash('Item updated.', 'success')
        return redirect(url_for('collections.view_collection', collection_id=str(item['collection_id'])))

    return render_template('items/item_form.html', collection=collection, item=item)


@items_bp.route('/<item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    db = current_app.db
    item = db.items.find_one({
        '_id': ObjectId(item_id),
        'user_id': _get_user_id()
    })
    if not item:
        flash('Item not found or access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    collection_id = str(item['collection_id'])
    db.items.delete_one({'_id': ObjectId(item_id)})
    flash('Item deleted.', 'success')
    return redirect(url_for('collections.view_collection', collection_id=collection_id))
