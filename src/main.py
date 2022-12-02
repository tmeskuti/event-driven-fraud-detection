import json
import base64
import functions_framework
from google.cloud import firestore

db = firestore.Client()
doc_ref = db.collection('messages')


# Register a CloudEvent function with the Functions Framework
@functions_framework.cloud_event
def subscribe(cloud_event):
    # Pull the message from the Pub/Sub queue in bytestring form
    message = base64.b64decode(cloud_event.data["message"]["data"])
    # Convert the message to a dictionary
    message_dict = json.loads(message)

    doc_ref.add(message_dict)
