# SMS Verification Project

A Python application for sending SMS messages through Huawei LTE modems/routers.

## Features

- Send SMS messages via Huawei LTE modem/router
- Simple and easy-to-use interface
- Error handling for connection issues
- Automatic session cleanup

## Requirements

- Python 3.7+
- Huawei LTE modem/router accessible at `http://192.168.8.1/`
- Network connection to the modem

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/SMS_Verification.git
cd SMS_Verification
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Update the `recipient_number` variable in `VerifySMS.py` with the target phone number (include country code)
2. Modify the `message` variable with your desired message content
3. Ensure your Huawei modem/router is accessible at the configured IP address
4. Run the script:
```bash
python VerifySMS.py
```

## Configuration

- **Modem IP**: Default is `http://192.168.8.1/`
- **Authentication**: Add credentials if your modem is password-protected: `http://admin:your_password@192.168.8.1/`

## Example

```python
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

# Connect to the modem
connection = Connection('http://192.168.8.1/')
client = Client(connection)

# Send SMS
recipient_number = '+1234567890'
message = 'Your verification code is: 123456'
client.sms.send_sms(recipient_number, message)
```

## Troubleshooting

- Ensure the modem is accessible on the network
- Check if the modem requires authentication
- Verify the recipient number format includes country code
- Check network connectivity to the modem

## License

This project is open source and available under the [MIT License](LICENSE).
