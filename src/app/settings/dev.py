from app.settings.components.base import *
from app.settings.components.database import *
from app.settings.components.dev_tools import *
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
STATIC_ROOT = os.path.join(BASE_DIR, 'cdn/static')
