import sys
sys.path.insert(0, '/var/www/flask_app')
sys.stdout = sys.stderr
from app import app
application = app
