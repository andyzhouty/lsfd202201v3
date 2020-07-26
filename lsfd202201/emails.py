import os
from threading import Thread
from mailjet_rest import Client
from flask import render_template

api_key = os.getenv("MAILJET_API_KEY")
api_secret = os.getenv("MAILJET_API_SECRET")
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def send_email(receiver: str, receiver_name: str, **kwargs) -> int:
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
                "TextPart":
                    render_template('admin_notifactions.txt',
                                    name=receiver_name, **kwargs),
                "HTMLPart":
                    render_template('admin_notifactions.html',
                                    name=receiver_name, **kwargs),
                "CustomID": "AritcleUploaded"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code


def send_async_email(*args, **kwargs) -> Thread:
    thd = Thread(target=send_email,
                 args=args,
                 kwargs=kwargs)
    thd.start()
    return thd
