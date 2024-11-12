# azure_backup/azure_backup/azure_helper.py
from datetime import timedelta
from datetime import datetime
import os
import frappe
from azure.storage.blob import BlobServiceClient
from frappe.utils import get_site_path, now_datetime, add_days
import logging
from frappe.utils import get_site_name

def get_azure_service_client():
    settings = frappe.get_single("Azure Backup Settings")
    account_name = settings.azure_account_name
    account_key = settings.get_password(fieldname="azure_account_key")
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    return blob_service_client
   
def upload_file_to_azure(file_path, blob_name):
    blob_service_client = get_azure_service_client()
    container_name = frappe.get_single("Azure Backup Settings").azure_container_name
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    print("executed")
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    
    frappe.logger().info(f"Uploaded {file_path} to Azure Blob Storage as {blob_name}.")
    
    if os.path.exists(file_path):
        file_name = file_path.split("/")[-1]
        os.remove(file_path)
        frappe.logger().info(f"Deleted local backup file: {file_path}")
    else:
        frappe.logger().warning(f"Local backup file not found for deletion: {file_path}")


    backup_directory = os.path.dirname(file_path)
    remaining_extensions = [".tar", ".json"]  

    for file in os.listdir(backup_directory):
        if file.endswith(tuple(remaining_extensions)):
            file_to_delete = os.path.join(backup_directory, file)
            try:
                os.remove(file_to_delete)
                frappe.logger().info(f"Deleted additional backup file: {file_to_delete}")
            except Exception as e:
                frappe.logger().error(f"Error deleting file {file_to_delete}: {e}")



def apply_retention_policy():
    settings = frappe.get_single("Azure Backup Settings")
    retention_days = settings.retention_days
    blob_service_client = get_azure_service_client()
    container_client = blob_service_client.get_container_client(settings.azure_container_name)

    blobs = container_client.list_blobs()
    cutoff_date = now_datetime() - timedelta(days=retention_days)
    # cutoff_date = now_datetime().replace(hour=0, minute=0, second=0, microsecond=0) - frappe.utils.timedelta(days=retention_days)

    for blob in blobs:
        # Extract timestamp from blob name assuming format backup_YYYYMMDD_HHMMSS.sql.gz
        try:
            # timestamp_str = blob.name.replace("backup_", "").replace(".sql.gz", "")
            time_data = blob.name.split('_')[1:3]
            timestamp_str = f'{time_data[0]}_{time_data[1][0:6]}'

            # blob_date = frappe.utils.get_datetime(timestamp_str, format="%Y%m%d_%H%M%S")
            blob_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")

            if blob_date < cutoff_date:
                blob_client = container_client.get_blob_client(blob)
                blob_client.delete_blob()
                frappe.logger().info(f"Deleted old backup blob: {blob.name}")
        except Exception as e:
            frappe.logger().error(f"Error parsing blob name {blob.name}: {e}")

# # 
# def get_azure_service_client():
#     settings = frappe.get_single("Azure Backup Settings")
#     account_name = settings.azure_account_name
#     account_key = settings.get_password(fieldname="azure_account_key")  # Securely fetch the password
#     connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
#     blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#     return blob_service_client
