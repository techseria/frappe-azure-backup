# Azure Backup Frappe App

## Overview

The Azure Backup app integrates Frappe/ERPNext with Azure Blob Storage to perform backups. It provides features such as email notifications, retention policies, secure storage of sensitive information, error recovery with retry mechanisms, manual backup options, and the ability to choose between backing up the database only or both database and files.

## Features

1. **Daily Backups:** Automatically performs daily backups at the configured time.
2. **Azure Integration:** Uploads backups to Azure Blob Storage.
3. **Email Notifications:** Sends daily emails indicating the success or failure of backups.
4. **Retention Policy:** Automatically deletes backups older than the specified number of days.
5. **Secure Storage:** Encrypts sensitive information like Azure Account Key.
6. **Error Recovery:** Implements retry mechanisms for transient errors.
7. **Manual Backup:** Allows administrators to trigger backups manually via the UI.
8. **Backup Type Selection:** Choose between backing up the database only or both database and files.
9. **User-Friendly Configuration:** Provides tooltips and an onboarding guide for easy setup.

## Installation

1. **Clone the Repository:**

    ```bash
    bench get-app https://github.com/techseria/frappe-azure-backup.git
    ```

2. **Install the App:**

    ```bash
    bench --site [your-site-name] install-app azure_backup
    ```

3. **Install Dependencies:**

    Navigate to the `azure_backup` directory and install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Access Azure Backup Settings:**

    - Navigate to **Settings > Azure Backup Settings** in your Frappe/ERPNext site.

2. **Fill in the Required Fields:**

    - **Enable Backup:** Check this box to enable backup functionalities.
    - **Backup Type:** Select either **Database Only** or **Database + Files**.
    - **Azure Account Name:** Your Azure Storage Account Name.
    - **Azure Account Key:** Your Azure Storage Account Key. This is encrypted and stored securely.
    - **Azure Container Name:** The name of the container in Azure Blob Storage where backups will be stored.
    - **Backup Frequency:** Select `Daily`.
    - **Backup Time:** Set the time for automated backups (e.g., `00:00` for midnight).
    - **Notification Emails:** Enter the email addresses that should receive backup notifications, separated by commas (e.g., `admin@example.com`).
    - **Retention Days:** Define how many days backups should be retained in Azure (e.g., `30`).

3. **Save the Settings:**

    After filling in all fields, click **Save** to apply the settings.

## Usage

- **Automatic Backups:** The app automatically schedules backups based on the configured time and type.
- **Manual Backup:** To manually trigger a backup, navigate to **Azure Backup Settings** and click the **Backup Now** button.

## Backup Type Selection

- **Database Only:** Backs up only the database. This is suitable for instances where file backups are managed separately or are not required.
- **Database + Files:** Backs up both the database and the files (e.g., uploaded documents, attachments). This ensures a complete backup of your Frappe/ERPNext instance.

## Troubleshooting

- **Backup Failures:** Check the email notifications for failure messages. Ensure that Azure credentials are correct and that the Azure Blob Storage container exists.
- **Email Issues:** Verify that the Frappe email settings are correctly configured to send emails.
- **Retention Policy Errors:** Ensure that the `retention_days` is set correctly and that the Azure account has permissions to delete blobs.

## Development

### Running Tests

To run unit tests, execute:

```bash
bench --site [your-site-name] run-tests --module azure_backup