# Custom Collectibles

A web-based collection management system with **dynamic custom fields**, ownership controls, and a public image gallery.

Built for an undergraduate Computing project (Arden University style).

## Features

- User registration & login (Flask-Login + bcrypt hashing)
- Categories and Collections (CRUD)
- Items with **runtime-defined custom fields** (text, number, date, boolean)
- Image upload and gallery
- Public / Private visibility for collections
- Public read-only gallery for non-owners
- Basic search across public collections and custom field values
- Responsive Bootstrap 5 UI

## Tech Stack

- Python 3.11+ / Flask 3
- MongoDB (document model with embedded `custom_fields` arrays)
- Bootstrap 5 + vanilla JavaScript (dynamic form builder)
- Pillow for image handling

## Quick Start (Local)

### 1. Prerequisites
- Python 3.11 or newer
- MongoDB running locally (`mongod`) or a MongoDB Atlas connection string

### 2. Setup
```bash
cd custom_collectibles
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment (optional)
Create a `.env` file:
```
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb://localhost:27017/custom_collectibles
```

### 4. Run
```bash
python app.py
```
Open http://127.0.0.1:5000

## Project Structure

```
custom_collectibles/
├── app.py                 # Application factory
├── config.py
├── requirements.txt
├── blueprints/
│   ├── auth.py            # Login / Register
│   ├── main.py            # Dashboard
│   ├── collections.py     # Categories & Collections
│   ├── items.py           # Items + dynamic custom fields
│   └── public.py          # Public gallery & search
├── templates/
├── static/
│   ├── css/
│   ├── js/dynamic_fields.js
│   └── uploads/
└── README.md
```

## How Dynamic Custom Fields Work

When a Collection Owner adds an item they can click **“+ Add Field”** any number of times.
Each field is stored in MongoDB as:

```json
"custom_fields": [
  { "field_name": "Grading", "field_type": "text", "value": "Near Mint" },
  { "field_name": "Year", "field_type": "number", "value": 1999 }
]
```

This realises the flexible schema designed in the project ERD without any schema migration.

## Matching the Report

This artefact implements the Must-Have requirements (FR-01 to FR-06) and the Should-Have search (FR-07) described in the final report.
