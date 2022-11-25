import base64
import functions_framework


# Register a CloudEvent function with the Functions Framework
@functions_framework.cloud_event
def subscribe(cloud_event):
    # Print out the data from Pub/Sub, to prove that it worked
    print("Hello, " + base64.b64decode(cloud_event.data["message"]["data"]).decode() + "!")
