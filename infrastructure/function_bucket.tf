resource "google_storage_bucket" "function_bucket" {
    name     = "${local.project}-function"
    location = local.region
}
