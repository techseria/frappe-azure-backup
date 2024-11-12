import frappe
import frappe.utils
from frappe.utils.backups import get_backup_path, scheduled_backup
from frappe.utils import get_datetime
from .azure_helper import upload_file_to_azure, apply_retention_policy
import os
from frappe import sendmail
from frappe.utils import get_site_name
import time
import logging
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import json
import zipfile

# Configure logger
logger = logging.getLogger(__name__)

@retry(
    retry=retry_if_exception_type(Exception),
    wait=wait_exponential(multiplier=2, min=4, max=10),
    stop=stop_after_attempt(3)
)

# def is_valid_zip(zip_file_path):
#     try:
#         with zipfile.ZipFile(zip_file_path) as z:
#             return z.testzip() is None  
#     except zipfile.BadZipFile:
#         return False


def upload_backup_to_azure():
    frappe.log_error(title="Test", message="Testing upload_backup_to_azure func ")
    settings = frappe.get_single("Azure Backup Settings")
    if not settings.enable_backup:
        frappe.logger().info("Azure Backup is disabled. Skipping backup process.")
        return 
    
    frappe.logger().info("Starting Azure backup process.")
    backup = scheduled_backup()

    if settings.backup_type == "Database Only":
        backup = scheduled_backup()
    elif settings.backup_type == "Database + Files":
        # backup = scheduled_backup(include_files=True)
        backup = scheduled_backup(ignore_files=False)

    else:
        frappe.logger().error(f"Invalid backup type selected: {settings.backup_type}")
        send_notification_email(status="Failed", error_message=f"Invalid backup type selected: {settings.backup_type}")
        return
    

    if not backup:
        frappe.logger().error("Backup failed during scheduled_backup.")
        send_notification_email(status="Failed", error_message="Backup failed during scheduled_backup.")
        return
    
    backup_file =  backup.backup_path_db if hasattr(backup, 'backup_path_db') else None
    
    if not backup_file or not os.path.exists(backup_file):
        frappe.logger().error("Backup file not found at path: {}".format(backup_file))
        send_notification_email(status="Failed", error_message="Backup file not found.")
        return
    site_name1 = get_site_name(frappe.local.site)
    timestamp = get_datetime().strftime("%Y%m%d_%H%M%S")

    if settings.backup_type == "Database + Files":
        # if not is_valid_zip(backup_file):
        #     frappe.logger().error("Backup ZIP file is invalid.")
        #     send_notification_email(status="Failed", error_message="Backup ZIP file is invalid.")
        #     return
        blob_name = f"{site_name1}_{timestamp}.zip"
    else:    
        blob_name = f"{site_name1}_{timestamp}.sql.gz"

    try:
        upload_file_to_azure(backup_file, blob_name)
        frappe.logger().info(f"Backup uploaded to Azure Blob Storage as {blob_name}.")
        send_notification_email(status="Success", blob_name=blob_name)
    except Exception as e:
        frappe.logger().error(f"Failed to upload backup to Azure: {e}")
        send_notification_email(status="Failed", error_message=str(e))
        raise  # To trigger retry

    # Apply retention policy after successful upload
    try:
        apply_retention_policy()
        frappe.logger().info("Retention policy applied successfully.")
    except Exception as e:
        frappe.logger().error(f"Failed to apply retention policy: {e}")
        # Optionally, notify admin about retention policy failure



def send_notification_email(status, blob_name=None, error_message=None):
    settings = frappe.get_single("Azure Backup Settings")
    recipients = settings.notification_emails.split(",")
    subject = f"Azure Backup {'Success' if status == 'Success' else 'Failure'} Notification"
    if status == "Success":
        message = f"The backup was successfully uploaded to Azure Blob Storage as {blob_name}."
    else:
        message = f"The backup process failed with the following error:\n\n{error_message}"
    
    try:
        print(recipients,blob_name)
        sendmail(
            recipients=[email.strip() for email in recipients],
            subject=subject,
            message=message,
            delayed=False
        )
        print("sent")
        frappe.logger().info(f"Notification email sent to {recipients}.")
    except Exception as e:
        frappe.logger().error(f"Failed to send notification email: {e}")



import frappe
from datetime import datetime

def update_backup_schedule(doc, method):
    backup_time = datetime.strptime(doc.backup_time, '%H:%M:%S').time()
    cron_expression = f"{backup_time.minute} {backup_time.hour} * * *"

    job_type_name = "tasks.upload_backup_to_azure"
    scheduled_job = frappe.get_doc("Scheduled Job Type", {"name": job_type_name}) if frappe.db.exists("Scheduled Job Type", job_type_name) else None

    if scheduled_job:
        scheduled_job.cron_format = cron_expression
        scheduled_job.save()
    else:
        frappe.get_doc({
            "doctype": "Scheduled Job Type",
            "name": job_type_name,
            "method": "azure_backup.tasks.upload_backup_to_azure",
            "cron_format": cron_expression,
            
        }).insert()

    # frappe.enqueue('frappe.utils.scheduler.start_scheduler',timeout = 10000)
    frappe.logger().info(f"Updated or created backup cron job: {cron_expression}")
