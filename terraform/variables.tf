locals {
  data_lake_bucket = "la_311"
}

variable "PROJECT_ID" {
  description = "Google Cloud project name"
  type = string
  default = "rare-deployment-385022"
}

variable "REGION" {
  description = "Region for GCP resources"
  default = "europe-west2"
  type = string
}

variable "STORAGE_CLASS" {
  description = "Storage class type for your bucket. Check official docs for more info"
  default = "STANDARD"
}

variable "BQ_DATASET_RAW" {
  description = "BigQuery Dataset where raw data from GCS will be written into"
  type = string
  default = "raw"
}

variable "BQ_DATASET_UAT" {
  description = "BigQuery Dataset where dbt dev models will be written into"
  type = string
  default = "uat"
}

variable "BQ_DATASET_PROD" {
  description = "BigQuery Dataset where dbt prod models will be written into"
  type = string
  default = "prod"
}