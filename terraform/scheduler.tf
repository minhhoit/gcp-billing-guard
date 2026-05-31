resource "google_cloud_scheduler_job" "reenable_monthly" {
  name      = "billing-reenable-monthly"
  schedule  = var.scheduler_schedule
  time_zone = var.scheduler_timezone
  region    = var.region

  http_target {
    uri         = google_cloudfunctions2_function.reenable_billing.service_config[0].uri
    http_method = "GET"

    oidc_token {
      service_account_email = google_service_account.billing_guard_sa.email
    }
  }
}
