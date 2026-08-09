gcp_project_id = "my-gcp-project"
gcp_region     = "US"

dataset_config = {
  dataset_id    = "my_simple_dataset"
  friendly_name = "My Simple Dataset"
  description   = "Dataset created via Terraform"
}

tables_config = {
  "table_one" = {
    table_id = "first_table"
  }
  "table_two" = {
    table_id = "second_table"
  }
}
