#!/bin/bash
set -e

echo "=== Test Disable Billing (Local Pub/Sub) ==="

PAYLOAD=$(cat tests/fixtures/payload_100_percent.json | base64)
gcloud pubsub topics publish billing-alerts --message="$PAYLOAD"

echo "Message published to billing-alerts topic."
echo "Check Cloud Function logs for results."
