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


def _delete_image_files(filenames):
    upload_dir = current_app.config['UPLOAD_FOLDER']
    for name in filenames or []:
        if not name:
            continue
        path = os.path.join(upload_dir, os.path.basename(str(name)))
        try:
            if os.path.isfile(path):
                os.remove(path)
        except OSError:
            pass


def invalid_image_message(file):
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        return 'Images must be PNG, JPG, JPEG, GIF or WEBP.'
    return None


def parse_custom_fields(form):
    custom_fields = []
    errors = []
    i = 0
    while True:
        name_key = f'field_name_{i}'
        if name_key not in form:
            break

        field_name = form.get(name_key, '').strip()
        field_type = form.get(f'field_type_{i}', 'text').strip()
        field_value = form.get(f'field_value_{i}', '').strip()

        if field_name:
            if field_type == 'number':
                if field_value == '':
                    errors.append(f'"{field_name}" must be a number.')
                else:
                    try:
                        field_value = float(field_value) if '.' in field_value else int(field_value)
                    except ValueError:
                        errors.append(f'"{field_name}" must be a valid number.')
            elif field_type == 'date':
                if field_value == '':
                    errors.append(f'"{field_name}" must be a date (YYYY-MM-DD).')
                else:
                    parsed = None
                    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'):
                        try:
                            parsed = datetime.strptime(field_value, fmt)
                            break
                        except ValueError:
                            continue
                    if parsed is None:
                        errors.append(f'"{field_name}" must be a valid date (use YYYY-MM-DD).')
                    else:
                        field_value = parsed.strftime('%Y-%m-%d')
            elif field_type == 'boolean':
                lowered = field_value.lower()
                if lowered in ('true', '1', 'yes', 'on'):
                    field_value = True
                elif lowered in ('false', '0', 'no', 'off'):
                    field_value = False
                else:
                    errors.append(f'"{field_name}" must be Yes or No.')

            custom_fields.append({
                'field_name': field_name,
                'field_type': field_type,
                'value': field_value
            })
        i += 1
    return custom_fields, errors


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

        custom_fields, field_errors = parse_custom_fields(request.form)
        if field_errors:
            for err in field_errors:
                flash(err, 'danger')
            return render_template('items/item_form.html', collection=collection)

        images = []
        if 'image' in request.files:
            file = request.files['image']
            img_error = invalid_image_message(file)
            if img_error:
                flash(img_error, 'danger')
                return render_template('items/item_form.html', collection=collection)
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
                images.append(unique_name)

        db.items.insert_one({
            'collection_id': ObjectId(collection_id),
            'user_id': _get_user_id(),
            'name': name,
            'custom_fields': custom_fields,
            'images': images,
            'created_at': datetime.utcnow()
        })
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

        custom_fields, field_errors = parse_custom_fields(request.form)
        if field_errors:
            for err in field_errors:
                flash(err, 'danger')
            return render_template('items/item_form.html', collection=collection, item=item)

        update = {
            'name': name,
            'custom_fields': custom_fields
        }

        if 'image' in request.files:
            file = request.files['image']
            img_error = invalid_image_message(file)
            if img_error:
                flash(img_error, 'danger')
                return render_template('items/item_form.html', collection=collection, item=item)
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
                _delete_image_files(item.get('images') or [])
                update['images'] = [unique_name]

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
    _delete_image_files(item.get('images') or [])
    db.items.delete_one({'_id': ObjectId(item_id)})
    flash('Item and its images have been deleted.', 'success')
    return redirect(url_for('collections.view_collection', collection_id=collection_id))
