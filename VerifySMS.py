#!/usr/bin/env python3
"""
SMS Verification System - Google Sheets Integration
Reads mobile numbers and verification codes from Google Sheets
and sends SMS verification messages automatically.
"""

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
import gspread
from google.oauth2.service_account import Credentials as ServiceCredentials
import time
from datetime import datetime

# Google Sheets setup
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

# You'll need to replace 'credentials.json' with your actual Google Sheets credentials file
creds = ServiceCredentials.from_service_account_file(
    'credentials.json', scopes=scopes)
client_gspread = gspread.authorize(creds)

# Replace with your actual Google Sheets ID
# You can find this in the URL of your Google Sheet
# Example: https://docs.google.com/spreadsheets/d/1PO894AzN9pzMFv4_wbF79UchaQsUU9_g8b5Xfs9wBxk/edit
# The ID is: 1PO894AzN9pzMFv4_wbF79UchaQsUU9_g8b5Xfs9wBxk

# TODO: Replace this with your actual Google Sheets ID
GOOGLE_SHEETS_ID = '1PO894AzN9pzMFv4_wbF79UchaQsUU9_g8b5Xfs9wBxk'

try:
    spreadsheet = client_gspread.open_by_key(GOOGLE_SHEETS_ID)
    print(f"Successfully connected to Google Sheet: {spreadsheet.title}")

    # List all available worksheets
    worksheets = spreadsheet.worksheets()
    print(f"Available worksheets: {[ws.title for ws in worksheets]}")

    # Try to access the 'Sheet2' worksheet (which contains the Caller data)
    try:
        sheet = spreadsheet.worksheet('Sheet2')
        print("Successfully connected to 'Sheet2' worksheet (Caller data)")
    except gspread.WorksheetNotFound:
        print("'Sheet2' worksheet not found!")
        print("Available worksheets:", [ws.title for ws in worksheets])
        print("Please create a worksheet named 'Sheet2' or update the code to use an existing worksheet")
        exit(1)

except gspread.SpreadsheetNotFound:
    print(f"Google Sheet with ID '{GOOGLE_SHEETS_ID}' not found!")
    print("Please check your Google Sheets ID and ensure the sheet is shared with your service account")
    exit(1)
except Exception as e:
    print(f"Error connecting to Google Sheet: {e}")
    print("Please check your credentials.json file and Google Sheets API setup")
    exit(1)

# Huawei LTE API setup


def initialize_huawei_client():
    """Initialize Huawei LTE client connection"""
    try:
        # Connect to the modem (use credentials if required)
        # Or 'http://admin:your_password@192.168.8.1/' if password-protected
        connection = Connection('http://192.168.8.1/')
        client = Client(connection)
        return client
    except Exception as e:
        print(f'Error initializing Huawei client: {e}')
        return None


def send_verification_sms(client, phone_number, verification_code):
    """Send SMS verification message"""
    try:
        message = f'Your verification code is {verification_code}'

        # Send the SMS
        client.sms.send_sms(phone_number, message)
        print(f'SMS sent successfully to {phone_number}: {message}')
        return True
    except Exception as e:
        print(f'Error sending SMS to {phone_number}: {e}')
        return False


def check_and_process_verifications():
    """Check Google Sheets for pending verifications and process them"""
    try:
        # Get all records from the sheet
        records = sheet.get_all_records()

        pending_count = 0
        processed_count = 0

        for idx, record in enumerate(records):
            try:
                # Check if status is "Pending"
                if record.get('Status', '').strip().lower() == 'pending':
                    pending_count += 1

                    # Get the data from the record
                    phone_number = str(record.get('Number', '')).strip()
                    verification_code = str(
                        record.get('Verify_Code', '')).strip()
                    record_id = record.get('ID', '')

                    # Validate the data
                    if not phone_number or not verification_code:
                        print(
                            f"Invalid data for ID {record_id}: Missing phone number or verification code")
                        continue

                    # Ensure phone number has country code if not already present
                    if not phone_number.startswith('+'):
                        if phone_number.startswith('0'):
                            phone_number = '+44' + \
                                phone_number[1:]  # UK number
                        else:
                            phone_number = '+44' + phone_number  # Add UK country code

                    print(
                        f"Processing verification for ID {record_id}: {phone_number}")

                    # Initialize Huawei client for this SMS
                    huawei_client = initialize_huawei_client()
                    if not huawei_client:
                        print(
                            f"Failed to initialize Huawei client for {phone_number}")
                        continue

                    try:
                        # Send the verification SMS
                        if send_verification_sms(huawei_client, phone_number, verification_code):
                            # Update status to "Done"
                            # Update Status column (4th column)
                            sheet.update_cell(idx + 2, 4, 'Done')
                            processed_count += 1
                            print(
                                f"Successfully processed verification for {phone_number}")
                        else:
                            # Update status to "Failed"
                            sheet.update_cell(idx + 2, 4, 'Failed')
                            print(f"Failed to send SMS to {phone_number}")

                    finally:
                        # Logout to clean up the session
                        try:
                            huawei_client.user.logout()
                        except:
                            pass

                    # Small delay between SMS to avoid overwhelming the modem
                    time.sleep(2)

            except Exception as e:
                print(f"Error processing record {idx}: {e}")
                continue

        if pending_count > 0:
            print(
                f"Processed {processed_count}/{pending_count} pending verifications")
        else:
            print("No pending verifications found")

    except Exception as e:
        print(f"Error checking Google Sheets: {e}")


def main():
    """Main function to run the SMS verification system"""
    print("=== SMS Verification System ===")
    print("Reading from Google Sheets 'Caller' worksheet")
    print("Monitoring for 'Pending' status in Status column")
    print("Sending verification SMS messages automatically")
    print("Checking every 30 seconds...")

    # Check if we have valid Google Sheets connection
    if 'sheet' not in globals():
        print("Google Sheets connection failed. Please check your configuration.")
        return

    try:
        while True:
            print(
                f"\n--- Checking at {datetime.now().strftime('%H:%M:%S')} ---")
            check_and_process_verifications()
            print("Waiting 30 seconds until next check...")
            time.sleep(15)  # Check every 30 seconds

    except KeyboardInterrupt:
        print("\nShutting down SMS verification system...")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()
