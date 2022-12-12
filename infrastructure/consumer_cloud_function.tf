# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "source" {
    type        = "zip"
    source_dir  = "../src"
    output_path = "/tmp/function.zip"
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "zip" {
    source       = data.archive_file.source.output_path
    content_type = "application/zip"

    # Append to the MD5 checksum of the files's content
    # to force the zip to be updated as soon as a change occurs
    name         = "src-${data.archive_file.source.output_md5}.zip"
    bucket       = google_storage_bucket.function_bucket.name

}

# Create the Cloud function triggered by a publishing messages to a Pub/Sub topic
resource "google_cloudfunctions2_function" "function" {
    name         = "consumer"
    location = var.region

    build_config {
        runtime = "python310"
        entry_point = "subscribe"
        source {
            storage_source {
                bucket = google_storage_bucket.function_bucket.name
                object = google_storage_bucket_object.zip.name
            }
        }
    }

    service_config {
        environment_variables = {
            _db_password="changeme",
            _db_user="user",
            _dbname="fd-database",
            instance_name="fd-instance",
            project_id=var.project_id
        }
    }

    event_trigger {
        event_type = "google.cloud.pubsub.topic.v1.messagePublished"
        pubsub_topic   = google_pubsub_topic.messages.id
    }

}