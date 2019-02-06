import firebase_admin
from firebase_admin import credentials

# cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
cred = credentials.Certificate("keys/firebase.json")
default_app = firebase_admin.initialize_app(cred)
