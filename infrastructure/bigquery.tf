resource "google_bigquery_dataset" "dataset" {
  dataset_id    = "fraud_detection"
  friendly_name = "fd"
  location      = var.region
}

resource "google_bigquery_table" "users" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "users"

  schema = <<EOF
[
  {
    "name": "user_id",
    "type": "INT64",
    "mode": "NULLABLE"
  },
  {
    "name": "region",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "email",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "hashed_password",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "memberships" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "memberships"

  schema = <<EOF
[
  {
    "name": "membership_id",
    "type": "INT64",
    "mode": "NULLABLE"
  },
  {
    "name": "user_id",
    "type": "INT64",
    "mode": "NULLABLE"
  },
  {
    "name": "membership_type",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "payment_type",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "checkins" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "checkins"

  schema = <<EOF
[
  {
    "name": "checkin_id",
    "type": "INT64",
    "mode": "NULLABLE"
  },
  {
    "name": "checkin_date",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "user_id",
    "type": "INT64",
    "mode": "NULLABLE"
  },
  {
    "name": "venue_id",
    "type": "INT64",
    "mode": "NULLABLE"
  },
  {
    "name": "activity",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "venue" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "venue"

  schema = <<EOF
[
  {
    "name": "venue_id",
    "type": "INT64",
    "mode": "NULLABLE"
  },
  {
    "name": "region",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "address",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "main_sport",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "fraud" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "fraud"

  schema = <<EOF
[
  {
    "name": "fraud_id",
    "type": "INT64",
    "mode": "NULLABLE"
  },
  {
    "name": "event_id",
    "type": "INT64",
    "mode": "NULLABLE"
  },
  {
    "name": "checkin_id",
    "type": "INT64",
    "mode": "NULLABLE"
  },
  {
    "name": "rule_type",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}