from google.cloud import pubsub_v1
import random
import json
import uuid

project_id = "sustained-drake-368613"
topic_id = "test_topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

if __name__ == "__main__":
    regions = ["Berlin", "Hamburg", "Munich", "Frankfurt", "Dusseldorf"]
    membership_types = ["S", "M", "L"]
    for n in range(1, 10):
        data = {
            "venue_id": str(uuid.uuid4()),
            "checkin_id": str(uuid.uuid4()),
            "booking_id": str(uuid.uuid4()),
            "venue_region": random.choice(regions),
            "sport_type": "Gym",
            "user": {
                "user_id": str(uuid.uuid4()),
                "user_region": random.choice(regions),
                "user_membership_type": random.choice(membership_types),
            },
        }

        # Data must be a bytestring
        data_json = json.dumps(data, indent=2).encode('utf-8')
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data=data_json)
        print(future.result())

    print("Published messages.")
