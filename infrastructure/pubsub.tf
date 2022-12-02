resource "google_pubsub_topic" "messages" {
  name = "messages_topic"
  message_retention_duration = "86600s"
}

resource "google_pubsub_subscription" "example" {
  name  = "evaluator-subscription"
  topic = google_pubsub_topic.messages.name

  ack_deadline_seconds = 20

}

