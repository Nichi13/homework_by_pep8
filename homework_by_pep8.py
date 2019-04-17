import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_SMTP = 'smtp.gmail.com'
GMAIL_IMAP = 'imap.gmail.com'


class Mail:

    def __init__(self, login, password, mail_smtp=GMAIL_SMTP, mail_imap=GMAIL_IMAP, header=None):
        self.login = login
        self.password = password
        self.GMAIL_PORT = mail_smtp
        self.IMAP = mail_imap
        self.header = header

    def send_message(self, subject, message, recipients):
        self.message = message
        message_send = MIMEMultipart()
        message_send['From'] = self.login
        message_send['To'] = ', '.join(recipients)
        message_send['Subject'] = subject
        message_send.attach(MIMEText(message))
        pass

    def client_indification(self):
        mail_client_indif = smtplib.SMTP(self.GMAIL_PORT, 587)
        self.mail_client_indif = mail_client_indif
        # identify ourselves to smtp gmail client
        mail_client_indif.ehlo()
        # secure our email with tls encryption
        mail_client_indif.starttls()
        # re-identify ourselves as an encrypted connection
        mail_client_indif.ehlo()
        pass

    def send_mail(self):
        self.mail_client_indif.login(self.login, self.password)
        self.mail_client_indif.sendmail(self.login,
                                        self.mail_client_indif, self.message.as_string())
        self.mail_client_indif.quit()
        pass

    def get_mail_for_client(self):
        get_mail = imaplib.IMAP4_SSL(self.IMAP)
        get_mail.login(self.login, self.password)
        get_mail.list()
        get_mail.select('inbox')
        criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
        result, data = get_mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = get_mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        get_mail.logout()
        return email_message


if __name__ == '__main__':
    s = Mail('login@gmail.com', 'qwerty')
    s.send_message('Subject', 'Message', recipients=['vasya@email.com', 'petya@email.com'])
    s.client_indification()
    s.send_mail()
    print(s.get_mail_for_client())
