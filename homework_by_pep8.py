import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:

    def __init__(self, login, password, subject, message, recipients, header=None):
        self.login = login
        self.password = password
        self.subject = subject
        self.message = message
        self.header = header
        self.recipients = recipients
        self.GMAIL_SMTP = 'smtp.gmail.com'
        self.GMAIL_IMAP = 'imap.gmail.com'

    def send_message(self):
        message = MIMEMultipart()
        message['From'] = self.login
        message['To'] = ', '.join(self.recipients)
        message['Subject'] = self.subject
        message.attach(MIMEText(self.message))
        pass

    # send message

    def client_indification(self):
        mail_client_indif = smtplib.SMTP(self.GMAIL_SMTP, 587)
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

    # send end
    # recieve

    def get_mail_for_client(self):
        get_mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
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


# end recieve


if __name__ == '__main__':
    s = Mail('login@gmail.com', 'qwerty', 'Subject',
             'Message', recipients=['vasya@email.com', 'petya@email.com'])
    s.send_message()
    s.client_indification()
    s.send_mail()
    print(s.get_mail_for_client())