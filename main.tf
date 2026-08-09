terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id    = var.dataset_config.dataset_id
  friendly_name = lookup(var.dataset_config, "friendly_name", null)
  description   = lookup(var.dataset_config, "description", null)
  location      = var.gcp_region
}

resource "google_bigquery_table" "tables" {
  for_each = var.tables_config

  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = each.value.table_id
  schema              = file("${path.module}/table.json")
  deletion_protection = false # Set to false to allow easy cleanup/testing
}
