// apps/azure_backup/azure_backup/doctype/azure_backup_settings/azure_backup_settings.js

frappe.ui.form.on('Azure Backup Settings', {
    refresh: function(frm) {
        frm.set_intro('Configure Azure Backup settings below. Ensure that the Azure Account Key is kept secure.');

        // Tooltips for each field
        frm.fields_dict.azure_account_name.input.setAttribute('title', 'Your Azure Storage Account Name.');
        frm.fields_dict.azure_account_key.input.setAttribute('title', 'Your Azure Storage Account Key. This is sensitive information.');
        frm.fields_dict.azure_container_name.input.setAttribute('title', 'The name of the Azure Blob Storage container where backups will be stored.');
        frm.fields_dict.backup_frequency.input.setAttribute('title', 'Frequency of backups. Currently, only Daily backups are supported.');
        frm.fields_dict.backup_time.input.setAttribute('title', 'Time of day when the backup should occur (24-hour format).');
        frm.fields_dict.notification_emails.input.setAttribute('title', 'Comma-separated email addresses to receive backup notifications.');
        frm.fields_dict.retention_days.input.setAttribute('title', 'Number of days to retain backups in Azure Blob Storage.');

        // Add "Backup Now" button
        frm.add_custom_button(__('Backup Now'), function() {
            if (frm.doc.enable_backup) {
                console.log(frm.doc.name)
                if (frm.doc.azure_account_name && frm.doc.azure_account_key && frm.doc.azure_container_name) {
                    frappe.confirm(
                        'Are you sure you want to perform a manual backup?',
                        function() {
                            frappe.call({
                                method: 'azure_backup.azure_backup.doctype.azure_backup_settings.azure_backup_settings.manual_backup',
                                doc_name:frm.doc,
                                freeze: true,
                                freeze_message: 'Performing backup...',
                                callback: function(r) {
                                    if (!r.exc) {
                                        frappe.msgprint(__('Backup process initiated. Check your email for notifications.'));
                                    }
                                }
                            });
                        },
                        function() {
                            // Action on Cancel
                        }
                    );
                } else {
                    frappe.throw(__('Please ensure all required fields are filled before performing a manual backup.'));
                }
            } else {
                frappe.throw(__('Backup functionality is disabled. Enable it to perform backups.'));
            }
        }, __('Actions'));
    }
});
