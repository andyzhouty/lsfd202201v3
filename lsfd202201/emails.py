from mailjet_rest import Client
import os
api_key = os.getenv("MAILJET_API_KEY")
api_secret = os.getenv("MAILJET_API_SECRET")
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def send_email(receiver: str, receiver_name: str, text: str, html: str) -> int:
    data = {
        'Messages': [
            {
                "From": {
                    "Email": os.getenv("DEFAULT_EMAIL_SENDER"),
                    "Name": os.getenv("DEFAULT_SENDER_NAME")
                },
                "To": [
                    {
                        "Email": receiver,
                        "Name": receiver_name
                    }
                ],
                "Subject": "A new article was uploaded",
                "TextPart": text,
                "HTMLPart": html,
                "CustomID": "AritcleUploaded"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code
