resource "google_service_account" "billing_guard_sa" {
  account_id   = "billing-guard-sa"
  display_name = "Billing Guard Service Account"
}

resource "google_project_iam_member" "log_writer" {
  project = var.gcp_project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.billing_guard_sa.email}"
}

resource "google_project_iam_member" "run_invoker" {
  project = var.gcp_project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.billing_guard_sa.email}"
}
