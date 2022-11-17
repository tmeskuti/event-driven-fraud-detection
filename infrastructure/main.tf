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
  project = local.project
  region = local.region
}

locals {
  project = "sustained-drake-368613"
  region = "europe-west3"
}
