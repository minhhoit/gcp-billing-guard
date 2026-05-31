# GCP Billing Guard

Tự động disable billing GCP khi tổng chi phí billing account đạt 100% budget. Tự động re-enable vào ngày 1 mỗi tháng.

## Architecture

```
GCP Budget Alert → Pub/Sub → disable-billing-fn (Cloud Function Gen2)
Cloud Scheduler (cron: 0 0 1 * *) → reenable-billing-fn (Cloud Function Gen2)
```

## Prerequisites

- GCP Project with billing enabled
- Terraform >= 1.5
- `gcloud` CLI authenticated
- Python 3.11

## Quick Start

### 1. Configure

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
# Edit terraform.tfvars with your project ID and billing account
```

Edit `config/projects.json` with your managed projects.

### 2. Deploy

```bash
chmod +x scripts/deploy_all.sh
./scripts/deploy_all.sh
```

### 3. Manual IAM Setup (one-time)

```bash
gcloud beta billing accounts add-iam-policy-binding XXXXXX-XXXXXX-XXXXXX \
  --member="serviceAccount:billing-guard-sa@YOUR_PROJECT.iam.gserviceaccount.com" \
  --role="roles/billing.projectManager"
```

### 4. GCP Console — Create Budget

1. Go to **Billing → Budgets & alerts → Create budget**
2. Name: `monthly-total-cost`
3. Scope: Billing account (no project filter)
4. Budget type: Specified amount
5. Amount: Your budget (e.g., 1,000,000 VND)
6. Threshold: 100% — Actual
7. Connect Pub/Sub topic: `billing-alerts`

## Testing

### Run unit tests
```bash
pip install pytest
pytest tests/
```

### Test disable function (sends Pub/Sub message)
```bash
chmod +x scripts/test_disable_local.sh
./scripts/test_disable_local.sh
```

### Test reenable function (calls HTTP endpoint)
```bash
chmod +x scripts/test_reenable_local.sh
./scripts/test_reenable_local.sh
```

## Project Structure

```
├── config/projects.json          # Master project list
├── functions/
│   ├── disable_billing/          # Pub/Sub trigger — disables billing
│   └── reenable_billing/         # HTTP trigger — re-enables billing
├── terraform/                    # Infrastructure as Code
├── scripts/                      # Deploy & test scripts
└── tests/                        # Unit tests
```

## How It Works

### Disable Flow
1. GCP Budget alert fires at 100% threshold
2. Pub/Sub message published to `billing-alerts` topic
3. `disable-billing-fn` triggered
4. Validates payload (costAmount, budgetAmount)
5. If cost/budget >= 1.0 → disables billing on all managed projects
6. Already-disabled projects are skipped

### Re-enable Flow
1. Cloud Scheduler fires at 00:00 on 1st of each month
2. HTTP GET to `reenable-billing-fn` with OIDC auth
3. For each project in config:
   - If billing OFF → re-enable
   - If billing ON → skip
4. Returns JSON summary with counts

## Adding Projects

Edit `config/projects.json`:
```json
{
  "billing_account_id": "XXXXXX-XXXXXX-XXXXXX",
  "projects": [
    {"project_id": "new-project-id", "display_name": "New Project"}
  ]
}
```

Then redeploy: `./scripts/deploy_all.sh`
