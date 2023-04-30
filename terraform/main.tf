terraform {
  required_version = ">= 1.0"
  backend "local" {} # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project     = var.PROJECT_ID
  region      = var.REGION
}

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.data_lake_bucket}"
  location      = var.REGION

  storage_class = var.STORAGE_CLASS
  uniform_bucket_level_access = true
  force_destroy = true

  versioning {
    enabled     = true
  }
}

resource "google_bigquery_dataset" "raw_dataset" {
  dataset_id = var.BQ_DATASET_RAW
  project    = var.PROJECT_ID
  location   = var.REGION
}

resource "google_bigquery_dataset" "uat_dataset" {
  dataset_id = var.BQ_DATASET_UAT
  project    = var.PROJECT_ID
  location   = var.REGION
}

resource "google_bigquery_dataset" "prod_dataset" {
  dataset_id = var.BQ_DATASET_PROD
  project    = var.PROJECT_ID
  location   = var.REGION
}