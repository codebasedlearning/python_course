# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about accessing Microsoft Exchange Services.

Teaching focus
  - read emails
  - send email

Preparations
  - .env file with credentials, not part of the project; entries e.g.,
        EXCHANGE_USER_NAME=xy1234z
  - virtual environment activated and libs installed, here,
        pip install exchangelib python-dotenv
"""

import os
from exchangelib import Credentials, Account, Message, Mailbox, FileAttachment
from dotenv import load_dotenv

load_dotenv()                               # load from .env


def query_mails_and_send_one():
    """ queries mails and sends one """
    print("\nquery_mails_and_send_one\n========================")

    try:
        print(f" 1| do not show credentials!")
        # from the terminal or in .env (without 'export'):
        #   export EXCHANGE_USER_NAME="username"
        #   export EXCHANGE_USER_PW="user pw"
        #   export EXCHANGE_USER_EMAIL="user email"
        user_name = os.getenv("EXCHANGE_USER_NAME")
        user_pw = os.getenv("EXCHANGE_USER_PW")
        user_email = os.getenv("EXCHANGE_USER_EMAIL")
        print(f" 2| we have: {user_name=}, pw ok? {user_pw is not None}, {user_email=}")

        credentials = Credentials(username=user_name, password=user_pw)
        print(f" 3| {credentials=}")

        account = Account(user_email, credentials=credentials, autodiscover=True)
        print(f" 4| {account=}")

        print(f" 5| query mails:")
        for item in account.inbox.all().order_by('-datetime_received')[:5]:
            print(f"    - from {item.sender.name}: '{item.subject[:25]}' received {item.datetime_received}")
            if item.attachments:  # I have seen Nones in the past...
                for attachment in item.attachments:
                    if isinstance(attachment, FileAttachment):
                        print(f"      * file '{attachment.name}' of size {attachment.size} bytes")

        print(f" 6| send mail")
        mail = Message(
            account=account,
            subject='Daily motivation',
            body='You are sooo good!',
            to_recipients=[
                Mailbox(email_address=user_email),
            ],
            # cc_recipients=[...
            # bcc_recipients=[...
        )
        # mail.send()
    except BaseException as e:
        print(f" 7| error {e})")


if __name__ == "__main__":
    query_mails_and_send_one()

"""
One might expect that ContextManagers also play a role here and that the classes 
support the protocol - but this is not the case. 

See
    https://pypi.org/project/exchangelib/
    https://ecederstrand.github.io/exchangelib/
"""
