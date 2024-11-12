# azure_backup/config/desktop.py

from frappe import _

def get_data():
    return [
        {
            "module_name": "Azure Backup",
            "color": "blue",
            "icon": "octicon octicon-cloud-upload",
            "type": "module",
            "label": _("Azure Backup")
        }
    ]
