output "disable_fn_url" {
  description = "URL of the disable billing function"
  value       = google_cloudfunctions2_function.disable_billing.service_config[0].uri
}

output "reenable_fn_url" {
  description = "URL of the reenable billing function"
  value       = google_cloudfunctions2_function.reenable_billing.service_config[0].uri
}

output "pubsub_topic" {
  description = "Pub/Sub topic ID for billing alerts"
  value       = google_pubsub_topic.billing_alerts.id
}

output "service_account" {
  description = "Service account email for billing guard"
  value       = google_service_account.billing_guard_sa.email
}
