# SMS Verification System - Setup Guide

## Prerequisites

1. **Google Sheets API Setup**
2. **Huawei LTE Modem Configuration**
3. **Python Dependencies Installation**

## Step 1: Google Sheets API Setup

### 1.1 Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Sheets API and Google Drive API

### 1.2 Create Service Account
1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Give it a name (e.g., "sms-verification-service")
4. Click "Create and Continue"
5. Skip role assignment for now
6. Click "Done"

### 1.3 Generate Credentials
1. Click on your created service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose "JSON" format
5. Download the JSON file and rename it to `credentials.json`
6. Place it in your project directory

### 1.4 Share Google Sheet
1. Open your Google Sheet with the "Caller" worksheet
2. Click "Share" button
3. Add the service account email (found in credentials.json) with "Editor" access
4. Copy the Google Sheets ID from the URL (the long string between `/d/` and `/edit`)

## Step 2: Configure the Code

### 2.1 Update Google Sheets ID
In `VerifySMS.py`, replace `YOUR_GOOGLE_SHEETS_ID_HERE` with your actual Google Sheets ID:

```python
spreadsheet = client_gspread.open_by_key(
    '1PO894AzN9pzMFv4_wbF79UchaQsUU9_g8b5Xfs9wBxk')  # Replace with your ID
```

### 2.2 Google Sheet Structure
Your "Caller" worksheet should have these columns:
- **ID**: Unique identifier
- **Number**: Mobile phone number (with or without country code)
- **Verify_Code**: 4-digit verification code
- **Status**: "Pending", "Sent", "Failed"

Example:
```
ID | Number        | Verify_Code | Status
1  | 07438000767   | 1234        | Pending
2  | +447438000768 | 5678        | Pending
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Huawei Modem Configuration

### 4.1 Network Access
- Ensure your Huawei LTE modem is accessible at `http://192.168.8.1/`
- If password-protected, update the connection string:
```python
connection = Connection('http://admin:your_password@192.168.8.1/')
```

### 4.2 Test Connection
Run a simple test to verify modem connectivity:
```python
python -c "
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
connection = Connection('http://192.168.8.1/')
client = Client(connection)
print('Connection successful!')
client.user.logout()
"
```

## Step 5: Run the System

```bash
python VerifySMS.py
```

The system will:
- Check Google Sheets every 30 seconds
- Look for rows with "Pending" status
- Send SMS with verification codes
- Update status to "Sent" or "Failed"

## Troubleshooting

### Common Issues:

1. **Authentication Error**
   - Verify `credentials.json` is in the project directory
   - Check service account has access to the Google Sheet

2. **Modem Connection Failed**
   - Verify modem IP address
   - Check network connectivity
   - Ensure modem is powered on

3. **Google Sheets Access Denied**
   - Share the sheet with service account email
   - Verify API permissions are enabled

4. **SMS Not Sending**
   - Check modem has SIM card and signal
   - Verify phone number format
   - Check modem SMS settings

## Status Values

- **Pending**: Waiting to be processed
- **Sent**: SMS sent successfully
- **Failed**: SMS sending failed

## Customization

### Change Check Interval
Modify the sleep time in the main loop:
```python
time.sleep(30)  # Change to desired seconds
```

### Modify SMS Message
Update the message format in `send_verification_sms()`:
```python
message = f'Your verification code is {verification_code}'
```

### Add Country Code Logic
The system automatically adds UK country code (+44) if missing. Modify the phone number processing logic as needed.
