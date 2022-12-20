resource "google_cloud_run_service" "producer" {
  name     = "producer"
  location = var.region

  template {
    spec {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/fraud-detection/event-producer"
      ports {
        container_port = 8501
      }
      env {
        name = "GOOGLE_PROJECT_ID"
        value = var.project_id
      }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_member" "member" {
  location = google_cloud_run_service.producer.location
  project = google_cloud_run_service.producer.project
  service = google_cloud_run_service.producer.name
  role = "roles/viewer"
  member = "user:teo@data-max.io"
}
