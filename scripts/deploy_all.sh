#!/bin/bash
set -e

echo "=== GCP Billing Guard - Full Deploy ==="

echo ""
echo "Step 1: Terraform Init"
terraform -chdir=terraform init

echo ""
echo "Step 2: Terraform Apply"
terraform -chdir=terraform apply -auto-approve

echo ""
echo "=== Deploy Complete ==="
echo "Disable Function URL: $(terraform -chdir=terraform output -raw disable_fn_url)"
echo "Reenable Function URL: $(terraform -chdir=terraform output -raw reenable_fn_url)"
echo "Service Account: $(terraform -chdir=terraform output -raw service_account)"
echo ""
echo "IMPORTANT: Don't forget to run the manual IAM binding:"
echo "  gcloud beta billing accounts add-iam-policy-binding <BILLING_ACCOUNT_ID> \\"
echo "    --member=\"serviceAccount:$(terraform -chdir=terraform output -raw service_account)\" \\"
echo "    --role=\"roles/billing.projectManager\""
