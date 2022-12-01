import json
import os
from datetime import date
from google.cloud import pubsub_v1
import uuid
import streamlit as st


project_id = "sustained-drake-368613"
topic_id = "test_topic"

# Create a Pub/Sub client to interact with the API
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Design the publisher interface using Streamlit
st.set_page_config(layout="centered", page_icon="📬", page_title="Message publisher")
st.title("Publisher")
st.write("Use the menu below to book a class!")
st.write("Fill in the data:")
form = st.form("template_form")
username = form.text_input("User name")
venue = form.selectbox(
    "Choose venue",
    ["Berlin", "Hamburg", "Munich", "Frankfurt", "Dusseldorf"],
    index=0,
)
activity = form.selectbox(
    "Choose class",
    ["Weightlifting 🏋️", "Boxing 🥊", "Swimming 🏊", "Tennis 🎾", "Yoga 🧘‍♀️", "Wrestling 🤼‍♂️"],
    index=0,
)
membership_type = form.radio("Select membership type", ["S", "M", "L"],
                             horizontal=True)

checkin_date = form.date_input("Select date")

submit = form.form_submit_button("Send message")

if submit:
    message = {
        "venue_id": str(uuid.uuid4()),
        "checkin_id": str(uuid.uuid4()),
        "booking_id": str(uuid.uuid4()),
        "venue": venue,
        "activity_type": activity,
        "checkin_date": str(checkin_date),
        "booking_timestamp": str(date.today().strftime("%B %d, %Y")),
        "user": {
            "user_id": str(uuid.uuid4()),
            "user_name": username,
            "user_membership_type": membership_type,
        },
    }

    # Data must be a bytestring
    data_bytes = json.dumps(message).encode('utf-8')
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data=data_bytes)
    print(future.result())

