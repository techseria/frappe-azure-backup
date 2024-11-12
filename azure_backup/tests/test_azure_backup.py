import frappe
import unittest
from azure_backup.tasks import upload_backup_to_azure, send_notification_email
from unittest.mock import patch, MagicMock
import os

class TestAzureBackup(unittest.TestCase):
    def setUp(self):
        self.settings = frappe.get_single("Azure Backup Settings")

    @patch('azure_backup.azure_backup.tasks.scheduled_backup')
    @patch('azure_backup.azure_backup.azure_helper.upload_file_to_azure')
    @patch('azure_backup.azure_backup.tasks.send_notification_email')
    def test_upload_backup_database_only_success(self, mock_send_email, mock_upload, mock_scheduled_backup):
        # Mock scheduled_backup to return a successful backup
        mock_scheduled_backup.return_value = MagicMock(backup_path="/path/to/backup.sql.gz")
        mock_upload.return_value = True

        # Mock os.path.exists to return True
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            upload_backup_to_azure()

            # Assert that upload was called
            mock_upload.assert_called_once_with("/path/to/backup.sql.gz", unittest.mock.ANY)
            # Assert that success email was sent
            mock_send_email.assert_called_once_with(status="Success", blob_name=unittest.mock.ANY)

    @patch('azure_backup.azure_backup.tasks.scheduled_backup')
    @patch('azure_backup.azure_backup.azure_helper.upload_file_to_azure')
    @patch('azure_backup.azure_backup.tasks.send_notification_email')
    def test_upload_backup_database_plus_files_success(self, mock_send_email, mock_upload, mock_scheduled_backup):
        # Change backup type to "Database + Files"
        self.settings.backup_type = "Database + Files"
        self.settings.save()

        # Mock scheduled_backup to return a successful backup
        mock_scheduled_backup.return_value = MagicMock(backup_path="/path/to/backup.zip")
        mock_upload.return_value = True

        # Mock os.path.exists to return True
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            upload_backup_to_azure()

            # Assert that upload was called with the correct blob name
            mock_upload.assert_called_once_with("/path/to/backup.zip", unittest.mock.ANY)
            # Assert that success email was sent
            mock_send_email.assert_called_once_with(status="Success", blob_name=unittest.mock.ANY)

    @patch('azure_backup.azure_backup.tasks.scheduled_backup')
    @patch('azure_backup.azure_backup.azure_helper.upload_file_to_azure')
    @patch('azure_backup.azure_backup.tasks.send_notification_email')
    def test_upload_backup_failure_backup(self, mock_send_email, mock_upload, mock_scheduled_backup):
        # Mock scheduled_backup to return None (failure)
        mock_scheduled_backup.return_value = None

        upload_backup_to_azure()

        # Assert that upload was not called
        mock_upload.assert_not_called()
        # Assert that failure email was sent
        mock_send_email.assert_called_once_with(status="Failed", error_message="Backup failed during scheduled_backup.")

    @patch('azure_backup.azure_backup.tasks.scheduled_backup')
    @patch('azure_backup.azure_backup.azure_helper.upload_file_to_azure')
    @patch('azure_backup.azure_backup.tasks.send_notification_email')
    def test_upload_backup_failure_upload(self, mock_send_email, mock_upload, mock_scheduled_backup):
        # Mock scheduled_backup to return a successful backup
        mock_scheduled_backup.return_value = MagicMock(backup_path="/path/to/backup.sql.gz")
        # Mock upload to raise an exception
        mock_upload.side_effect = Exception("Upload failed.")

        # Mock os.path.exists to return True
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            upload_backup_to_azure()

            # Assert that upload was called
            mock_upload.assert_called_once_with("/path/to/backup.sql.gz", unittest.mock.ANY)
            # Assert that failure email was sent
            mock_send_email.assert_called_once_with(status="Failed", error_message="Upload failed.")

    @patch('azure_backup.azure_backup.azure_helper.get_azure_service_client')
    def test_apply_retention_policy(self, mock_service_client):
        # Mock blobs with varying dates
        mock_blob_client = MagicMock()
        mock_container_client = MagicMock()
        mock_container_client.list_blobs.return_value = [
            MagicMock(name="backup_20230101_000000.sql.gz"),
            MagicMock(name="backup_20231231_235959.zip")
        ]
        mock_service_client.return_value.get_container_client.return_value = mock_container_client

        from azure_backup.azure_helper import apply_retention_policy

        apply_retention_policy()

        # Assert that delete_blob was called for the old backup
        mock_container_client.get_blob_client.assert_called_with("backup_20230101_000000.sql.gz")
        mock_blob_client.delete_blob.assert_called_once()

    @patch('azure_backup.azure_backup.tasks.scheduled_backup')
    def test_backup_disabled(self, mock_scheduled_backup):
        self.settings.enable_backup = 0
        self.settings.save()

        upload_backup_to_azure()

        # Assert that scheduled_backup was not called
        mock_scheduled_backup.assert_not_called()
