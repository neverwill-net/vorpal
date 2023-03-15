from flask import Flask
from media.database import get_session
from media.models import MediaFile
import uuid

app = Flask(__name__)

# Import routes and converters
from routes import *
from converters import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

