resource "google_pubsub_topic" "example" {
  name = "test_topic"
  message_retention_duration = "86600s"
}

resource "google_pubsub_subscription" "example" {
  name  = "evaluator-subscription"
  topic = google_pubsub_topic.example.name

  ack_deadline_seconds = 20

}

