import base64
import functions_framework
import json
from google.cloud import bigquery, firestore
import os

fs = firestore.Client()
doc_ref = fs.collection("events")

bq = bigquery.Client()


@functions_framework.cloud_event
def subscribe(cloud_event):
    event = base64.b64decode(cloud_event.data["message"]["data"])
    event_dict = json.loads(event)
    print(event_dict)
    doc_ref.add(event_dict)
    email_msg = event_dict["user"]["email"]
    date_msg = event_dict["checkin_date"]
    # Firstly the event is stored in Firestore as a document

    query = f"""
        select c.user_id, u.email, checkin_date, count(distinct v.region) as region_count
        from `fraud_detection.checkins` as c join `fraud_detection.venue` as v using (venue_id) join `fraud_detection.users`
        as u on c.user_id = u.user_id
        where u.email = '{email_msg}' and c.checkin_date = '{date_msg}'
        group by 1,2, 3;
    """
    print(f"query {query}")
    query_job = bq.query(query)

    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        print(f"Number of regions per user per day: {row.region_count}")
