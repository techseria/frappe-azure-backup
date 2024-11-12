# Copyright (c) 2024, Your Name and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document



class AzureBackupSettings(Document):
    pass

@frappe.whitelist()
def manual_backup(doc_name = None):
	from azure_backup.tasks import upload_backup_to_azure
	upload_backup_to_azure()
