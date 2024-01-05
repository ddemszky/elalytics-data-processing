import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize the Firestore client
cred = credentials.Certificate('./serviceAccountKey.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
