from flask import Flask
import os

app = Flask(__name__)

from views import *

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000, use_reloader=True, threaded=True)


