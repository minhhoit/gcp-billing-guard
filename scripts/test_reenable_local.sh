#!/bin/bash
set -e

echo "=== Test Reenable Billing (HTTP) ==="

FUNCTION_URL=$(terraform -chdir=terraform output -raw reenable_fn_url)
TOKEN=$(gcloud auth print-identity-token)

echo "Calling: $FUNCTION_URL"
curl -s -H "Authorization: Bearer $TOKEN" "$FUNCTION_URL" | python3 -m json.tool
