resource "google_cloudfunctions2_function" "disable_billing" {
  name     = var.disable_function_name
  location = var.region

  build_config {
    runtime     = "python311"
    entry_point = "disable_billing_handler"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.disable_billing_src.name
      }
    }
  }

  service_config {
    service_account_email = google_service_account.billing_guard_sa.email
    environment_variables = {
      CONFIG_PATH         = "./config/projects.json"
      TELEGRAM_BOT_TOKEN  = var.telegram_bot_token
      TELEGRAM_CHAT_ID    = var.telegram_chat_id
    }
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.billing_alerts.id
    retry_policy   = "RETRY_POLICY_DO_NOT_RETRY"
  }
}

resource "google_cloudfunctions2_function" "reenable_billing" {
  name     = var.reenable_function_name
  location = var.region

  build_config {
    runtime     = "python311"
    entry_point = "reenable_billing"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.reenable_billing_src.name
      }
    }
  }

  service_config {
    service_account_email = google_service_account.billing_guard_sa.email
    environment_variables = {
      CONFIG_PATH = "./config/projects.json"
    }
  }
}
