from . import observer_frontend, request_maker, forms
import os


def run(port=5000):
    observer_frontend.app.secret_key = os.urandom(12)
    observer_frontend.app.run(debug=False, host='0.0.0.0', port=port)
