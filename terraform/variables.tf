variable "gcp_project_id" {
  description = "GCP project that hosts the Cloud Functions"
  type        = string
}

variable "billing_account_id" {
  description = "GCP Billing Account ID"
  type        = string
}

variable "region" {
  description = "GCP region for resource deployment"
  type        = string
  default     = "asia-southeast1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "asia-southeast1-a"
}

variable "pubsub_topic_name" {
  description = "Pub/Sub topic name for billing alerts"
  type        = string
  default     = "billing-alerts"
}

variable "disable_function_name" {
  description = "Name of the disable billing Cloud Function"
  type        = string
  default     = "disable-billing-fn"
}

variable "reenable_function_name" {
  description = "Name of the reenable billing Cloud Function"
  type        = string
  default     = "reenable-billing-fn"
}

variable "scheduler_timezone" {
  description = "Timezone for Cloud Scheduler"
  type        = string
  default     = "Asia/Ho_Chi_Minh"
}

variable "scheduler_schedule" {
  description = "Cron schedule for monthly re-enable"
  type        = string
  default     = "0 0 1 * *"
}

variable "telegram_bot_token" {
  description = "Telegram Bot API token for notifications"
  type        = string
  sensitive   = true
}

variable "telegram_chat_id" {
  description = "Telegram Chat ID to send notifications to"
  type        = string
  default     = "8281492512"
}
