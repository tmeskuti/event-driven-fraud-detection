import json
import os
import uuid
from datetime import datetime
from google.cloud import pubsub_v1
import streamlit as st


project_id = os.getenv("GOOGLE_PROJECT_ID")
topic_id = "messages_topic"

# Create a Pub/Sub client to interact with the API
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Design the publisher interface using Streamlit
st.set_page_config(layout="centered", page_icon="📬", page_title="Message publisher")
st.title("Publisher")
st.write("Use the menu below to book a class!")

st.write("Fill in the data:")
form = st.form("template_form")
email = form.text_input("Email")
venue = form.selectbox(
    "Choose venue",
    ["Berlin", "Hamburg", "Munich", "Frankfurt", "Dusseldorf"],
    index=1,
)
activity = form.selectbox(
    "Choose class",
    ["Weightlifting", "Boxing", "Swimming", "Tennis", "Yoga", "Wrestling"],
    index=1,
)

checkin_date = form.date_input("Select date")
checkin_time = form.time_input("Select time")

submit = form.form_submit_button("Confirm")

if submit:
    message = {
        "checkin_id": str(uuid.uuid4()),
        "venue": venue,
        "activity_type": activity,
        "checkin_date": str(checkin_date),
        "checkin_time": str(checkin_time),
        "booking_timestamp": str(datetime.now()),
        "user": {
            "email": email
        },
    }

    # Data must be a bytestring
    data_bytes = json.dumps(message).encode('utf-8')
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data=data_bytes)
    print(future.result())

