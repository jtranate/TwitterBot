import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from bot_settings import EMAIL as settings

class Settings:
    enabled = None
    server_host = None
    server_port = None
    server_username = None
    server_password = None
    server_use_tls = False
    server_use_ssl = False
    sender = None
    to = None
    subject = None

def send(message):
  if not Settings.enabled:
    print("Emailer not enabled")
    return

  if not Settings.server_use_ssl:
    server = smtplib.SMTP(Settings.server_host, Settings.server_port)
  else:
    server = smtplib.SMTP_SSL(Settings.server_host, Settings.server_port)

  if Settings.server_use_tls:
    server.ehlo()
    server.starttls()
    server.ehlo()

  if Settings.server_username:
    server.login(Settings.server_username, Settings.server_password)

  msg = MIMEText(message)
  msg['From'] = Settings.sender
  msg['To'] = ', '.join(Settings.to)
  msg['Subject'] = Settings.subject

  server.sendmail(Settings.sender, Settings.to, msg.as_string())

  server.quit()


def setup():
    Settings.server_host = settings['SMTP_HOST']
    Settings.server_port = settings['PORT']
    Settings.server_username = settings['USERNAME']
    Settings.server_password = settings['PASSWORD']
    Settings.server_use_tls = settings['USE_TLS']
    Settings.server_use_ssl = settings['USE_SSL']
    Settings.sender = settings['FROM_ADDR']
    Settings.to = settings['TO']
    Settings.enabled = settings['ENABLED']
    Settings.subject = 'TWITTER BOT'
