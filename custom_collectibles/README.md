# Custom Collectibles

Web application for personal catalogues with **owner-defined item fields**, image uploads, and an optional public gallery.

Undergraduate Computing artefact (Arden University). Live demo: <http://209.42.23.78>  
Source: <https://github.com/vprata/arden-artefact>

## Stack

- Python 3.12 / Flask 3.0.3
- MongoDB 7 (document model)
- Flask-Login, PyMongo, Werkzeug, Pillow
- Bootstrap 5.3 and `static/js/dynamic_fields.js`
- Production: Ubuntu 24.04, Gunicorn, Nginx

## Project layout

```
custom_collectibles/
├── app.py                 # Flask factory, 413 handler
├── config.py
├── requirements.txt
├── blueprints/
│   ├── auth.py            # Register / login / logout
│   ├── main.py            # Owner dashboard
│   ├── collections.py     # Categories and user collections (incl. delete + image cleanup)
│   ├── items.py           # Items and parse_custom_fields()
│   └── public.py          # Public gallery and search
├── templates/
├── static/
│   ├── css/style.css
│   └── js/dynamic_fields.js
└── README.md
```

Uploaded images and `venv/` are not part of Git.

## How custom fields are stored

```json
"custom_fields": [
  { "field_name": "Author", "field_type": "text", "value": "Stoker" },
  { "field_name": "Number of pages", "field_type": "number", "value": 418 },
  { "field_name": "Date published", "field_type": "date", "value": "1897-05-26" },
  { "field_name": "First edition", "field_type": "boolean", "value": false }
]
```

`parse_custom_fields` in `blueprints/items.py` validates type before the document is written. Deleting a user collection (`delete_collection` in `blueprints/collections.py`) removes its items in MongoDB and the image files on disk.

## Requirements covered

Must-Have FR-01–FR-06 (auth, categories, user collections, typed custom fields, item CRUD + images, public gallery) and Should-Have FR-07 (search). See the project report for tests T-01–T-25.
