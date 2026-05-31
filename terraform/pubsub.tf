resource "google_pubsub_topic" "billing_alerts" {
  name = var.pubsub_topic_name
}

# Note: GCP Budget notifications publish to Pub/Sub automatically
# when configured via Console. The billing notification service identity
# is granted publisher access implicitly by the budget notification setup.
# No explicit IAM binding needed here.
