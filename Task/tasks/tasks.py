from .models import Task, Report
from django.core.mail import send_mail
from celery import current_app, shared_task
from celery.schedules import crontab
from celery.utils.log import get_logger
from django.contrib.auth.models import User
from django.db.models import Count
from django.db import transaction
from datetime import datetime, timedelta, timezone

logger = get_logger(__name__)
def send_report(user):
  status = (
    Task.objects.filter(user=user, deleted=False)
    .order_by("priority")
    .values("status")
    .annotate(count=Count("status"))
  )
  report = f"Hello, {user.username}. Daily Report:\n"
  if not status:
    report += "No task to report today."
  else:
    for s in status:
      _sn = s["status"].title().replace("-", " ")
      _sc = s["count"]
      report += f"{_sn} task{'s'[:_sc^1]}: {_sc}\n"
  send_mail("Daily Task Report", report, "example@example.com", ["dummy@user.com"])

@shared_task
def fetch_report():
  logger.info("fetch_settings: Started...")
  start = datetime.now(timezone.utc) - timedelta(days=2)
  logger.info(f"{start}\n")
  report_set = Report.objects.filter(
    send_report=True,
    last_updated__gt=start,
  )
  logger.info(f"fetch_report: {len(report_set)} users to report")
  with transaction.atomic():
    for report in report_set:
      send_report(report.user)
      report.last_updated = datetime.now(timezone.utc).replace(
        hour=report.time.hour, minute=report.time.minute, second=report.time.second)
      report.save()


@current_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.conf.beat_schedule["fetch_report"] = {
    "task": "tasks.tasks.fetch_report",
    "schedule": crontab(minute="*"),
  }