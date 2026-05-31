# Copilot Context — GCP Billing Guard

## Objective
Automatically disable GCP billing when total cost on a billing account reaches 100% of the budget.
Automatically re-enable at 00:00 on the 1st of each month.

## Stack
- Python 3.11, Cloud Functions Gen2, Pub/Sub, Cloud Scheduler, Terraform >= 1.5

## Important Rules
- disable_billing() must always return normally, never raise exceptions
  (prevents infinite Pub/Sub retry loops)
- reenable_billing() must always return HTTP 200 + JSON summary
- All logs must be JSON structured
- No projectId in payload = billing account level alert → disable ALL projects
- Master project list stored in config/projects.json
- Billing OFF → skip re-enable
- Billing ON  → skip disable

## Key Files
- config/projects.json       — master list, add new projects here
- terraform/terraform.tfvars — do not commit, create from .tfvars.example
