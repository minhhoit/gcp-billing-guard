# Copilot Context — GCP Billing Guard

## Mục tiêu
Tự động disable billing GCP khi tổng chi phí billing account đạt 100% budget.
Tự động re-enable lúc 00:00 ngày 1 hàng tháng.

## Stack
- Python 3.11, Cloud Functions Gen2, Pub/Sub, Cloud Scheduler, Terraform >= 1.5

## Quy tắc quan trọng
- Hàm disable_billing() luôn return bình thường, không raise exception
  (tránh Pub/Sub retry vô hạn)
- Hàm reenable_billing() trả về HTTP 200 + JSON summary mọi trường hợp
- Tất cả log dưới dạng JSON structured
- projectId không có trong payload = billing account level alert → disable TẤT CẢ
- Master list projects lưu trong config/projects.json
- Billing OFF → skip re-enable
- Billing ON  → skip disable

## File quan trọng nhất
- config/projects.json       — master list, thêm project mới vào đây
- terraform/terraform.tfvars — không commit, tạo từ .tfvars.example
