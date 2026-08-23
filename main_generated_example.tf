resource "google_bigquery_dataset" "storage" {
  dataset_id = "ent_data_wh"
  project = "my-gcp-project"
  location = "US"
  friendly_name = "Enterprise data warehouse"
  description = "Curated views for enterprise reporting"
  labels = {
    env = "prod"
    team = "data-platform"
  }
  default_table_expiration_ms = 31536000000
  default_partition_expiration_ms = 2592000000
  max_time_travel_hours = 96
  is_case_insensitive = false
  storage_billing_model = "LOGICAL"
  deletion_policy = "DELETE"
  delete_contents_on_destroy = false

  access {
    role = "OWNER"
    user_by_email = "bq-storage-sa@my-gcp-project.iam.gserviceaccount.com"
  }
  access {
    role = "READER"
    domain = "example.com"
  }
}
