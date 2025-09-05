from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

# Connect to the modem (use credentials if required)
# Or 'http://admin:your_password@192.168.8.1/' if password-protected
connection = Connection('http://192.168.8.1/')
client = Client(connection)

# Replace with recipient's number (include country code)
recipient_number = '+447438000767'
message = 'This is a test message.'

try:
    # Send the SMS
    client.sms.send_sms(recipient_number, message)
    print('SMS sent successfully')
except Exception as e:
    print(f'Error sending SMS: {e}')
finally:
    # Logout to clean up the session
    client.user.logout()
