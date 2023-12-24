'''pyhton built-in stmp server'''
from smtpd import SMTPServer
from email.message import EmailMessage
import asyncore
from typing import Any

class CustomSMTPServer(SMTPServer):
    def process_message(self, peer, mailfrom: str, rcpttos: list[str], data: bytes | str, **kwargs: Any) -> str | None:
        msg = EmailMessage()
        msg.set_content(data)
        msg['Subject'] = 'Password reset'
        msg['From'] = 'enememka@gmail.com'
        msg['To'] = ', '.join(rcpttos)
        print(msg.as_string())
        return super().process_message(peer, mailfrom, rcpttos, data, **kwargs)

if __name__ == '__main__':
    server = CustomSMTPServer(('localhost', 25), None)
    print('SMTP Server Started')
    asyncore.loop()