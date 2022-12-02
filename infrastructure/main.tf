terraform {
  backend "gcs" {
    bucket = "tm-fraud-detection-tfstate"
  }
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.43.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region = var.region
}