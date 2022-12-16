import base64
import functions_framework
import json
from google.cloud import bigquery, firestore

# Create the Firestore client and collection
fs = firestore.Client()
doc_ref = fs.collection("events")

# Create the BigQuery client
bq = bigquery.Client()


@functions_framework.cloud_event
def subscribe(cloud_event):
    event = base64.b64decode(cloud_event.data["message"]["data"])
    event_dict = json.loads(event)
    print(event_dict)

    # Firstly the event is stored in Firestore as a document
    doc_ref.add(event_dict)
    # We then extract the fields we need from the message
    email_msg = event_dict["user"]["email"]
    date_msg = event_dict["checkin_date"]
    activity_msg = event_dict["activity_type"]
    id_msg = event_dict["checkin_id"]
    region_msg = event_dict["venue"]

    # Insert message in the checkins table
    insert1 = bq.query(f""" 
        insert into fraud_detection.checkins
        select distinct '{id_msg}', date('{date_msg}'), user_id, venue_id, '{activity_msg}' 
        from `fraud_detection.users` join `fraud_detection.venue` using (region)
        where email = '{email_msg}'
    """)

    print(f"insertion: {insert1.result()}")

    # insert2 = bq.query(f"""
    #         insert into fraud_detection.checkins c (venue_id)
    #         select venue_id
    #         from `fraud_detection.venue`
    #         where region = '{region_msg}' and venue_id is null  """)
    #
    # print(f"insertion: {insert2.result()}")

    rule1 = f"""
        select c.user_id, u.email, checkin_date, count(distinct v.region) as region_count
        from `fraud_detection.checkins` as c join `fraud_detection.venue` as v using (venue_id) join `fraud_detection.users`
        as u on c.user_id = u.user_id
        where u.email = '{email_msg}' and c.checkin_date = '{date_msg}'
        group by 1, 2, 3;
    """

    result1 = "region_count"

    rule2 = f"""
        select user_id, email, checkin_date, count(*) as checkins_outside
        from `fraud_detection.users` as u join `fraud_detection.checkins` as c using (user_id)
        join `fraud_detection.venue` as v on v.venue_id = c.venue_id
        where u.email = '{email_msg}' and u.region != v.region
        group by 1, 2, 3
        order by checkin_date asc limit 3
    """

    result2 = "checkins_outside"

    rule3 = f"""
        select c.user_id, u.email, checkin_date, count(*) checkins_day
        from `fraud_detection.checkins` as c join `fraud_detection.venue` as v using (venue_id) join `fraud_detection.users`
        as u on c.user_id = u.user_id
        where u.email = '{email_msg}'
        group by 1, 2, 3;
    """

    result3 = "checkins_day"

    rule4 = f"""
        select user_id, email, count(distinct activity) > 5 as exceeded_activities
        from `fraud_detection.users` join `fraud_detection.checkins` using (user_id)
        where email = '{email_msg}' and checkin_date > DATE_SUB('{date_msg}', INTERVAL 14 day)
        group by 1, 2
    """

    result4 = "exceeded_activities"

    rules = [rule1, rule2, rule3, rule4]
    results = [result1, result2, result3, result4]
    values = []

    for rule, result in zip(rules, results):
        print(f"query: {rule}")
        print(f"result: {result}")
        query_job = bq.query(rule)
        rows = query_job.result()  # Waits for query to finish

        for row in rows:
            print(f'last row {row[result]}')
            values.append(row[result])

    print(values)

