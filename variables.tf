variable "gcp_project_id" {
  type        = string
  description = "The Google Cloud Project ID where resources will be created."
}

variable "gcp_region" {
  type        = string
  description = "The region/location for BigQuery resources."
  default     = "US"
}

variable "dataset_config" {
  type = object({
    dataset_id    = string
    friendly_name = optional(string)
    description   = optional(string)
  })
  description = "Configuration block for the BigQuery dataset."
}

variable "tables_config" {
  type = map(object({
    table_id = string
  }))
  description = "Configuration block for BigQuery tables."
}
