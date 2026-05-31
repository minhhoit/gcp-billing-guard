resource "google_storage_bucket" "function_source" {
  name                        = "${var.gcp_project_id}-billing-guard-src"
  location                    = var.region
  uniform_bucket_level_access = true
}

data "archive_file" "disable_billing_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../functions/disable_billing"
  output_path = "${path.module}/.tmp/disable_billing.zip"
}

data "archive_file" "reenable_billing_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../functions/reenable_billing"
  output_path = "${path.module}/.tmp/reenable_billing.zip"
}

resource "google_storage_bucket_object" "disable_billing_src" {
  name   = "disable_billing_${data.archive_file.disable_billing_zip.output_md5}.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.disable_billing_zip.output_path
}

resource "google_storage_bucket_object" "reenable_billing_src" {
  name   = "reenable_billing_${data.archive_file.reenable_billing_zip.output_md5}.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.reenable_billing_zip.output_path
}
