import json
import logging
import os
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


def notify_billing_disabled(project_id: str, cost_amount: float, budget_amount: float, scope: str):
    """Send Telegram notification when billing is disabled."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram not configured, skipping notification")
        return

    pct = (cost_amount / budget_amount * 100) if budget_amount > 0 else 0
    message = (
        f"🚨 <b>Billing Disabled</b>\n\n"
        f"<b>Project:</b> <code>{project_id}</code>\n"
        f"<b>Cost:</b> {cost_amount:,.0f}\n"
        f"<b>Budget:</b> {budget_amount:,.0f}\n"
        f"<b>Usage:</b> {pct:.0f}%\n"
        f"<b>Scope:</b> {scope}"
    )

    _send_telegram(message)


def notify_billing_disabled_summary(project_ids: list[str], cost_amount: float, budget_amount: float, scope: str):
    """Send a single summary notification for all disabled projects."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram not configured, skipping notification")
        return

    if not project_ids:
        return

    pct = (cost_amount / budget_amount * 100) if budget_amount > 0 else 0
    projects_list = "\n".join(f"  • <code>{p}</code>" for p in project_ids)
    message = (
        f"🚨 <b>Billing Guard Alert</b>\n\n"
        f"Đã disable billing cho <b>{len(project_ids)}</b> project(s):\n"
        f"{projects_list}\n\n"
        f"<b>Cost:</b> {cost_amount:,.0f} | <b>Budget:</b> {budget_amount:,.0f} ({pct:.0f}%)\n"
        f"<b>Scope:</b> {scope}"
    )

    _send_telegram(message)


def _send_telegram(message: str):
    """Send message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                logger.info("Telegram notification sent")
            else:
                logger.error(f"Telegram API returned {resp.status}")
    except urllib.error.URLError as e:
        logger.error(f"Failed to send Telegram notification: {e}")
