import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2026'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/custom_collectibles'
    UPLOAD_FOLDER = '/home/collectibles/uploads'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    SESSION_TIMEOUT_MINUTES = 30
