"""
    Wrapper module of python smtplib that handles mail sending operations
"""


from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class EmailSender():

    def __init__(self, configuration):
        try:
            self.email_sender = configuration.get("sender")
            self.email_password = configuration.get("password")
            self.smtp_host = configuration.get("host")
            self.smtp_port = configuration.get("port")

            # mixed : used to handle case where plain and html text are sent together
            self.email_message = MIMEMultipart('mixed')

            self.image_attachement_id_counter = 0
        except Exception as e:
            raise Exception(f'Error with the object configuration passed: {str(e)}')


    def set_sender_configuration(self, email_sender, email_password):
        try:
            self.email_sender = email_sender
            self.email_password = email_password
        except Exception as e:
            raise Exception(f"Eroor in parameters: {str(e)}")


    def set_host_configuration(self, smtp_host, smtp_port):
        try:
            self.smtp_host = smtp_host
            self.smtp_port = smtp_port
        except Exception as e:
            raise Exception(f"Eroor in parameters: {str(e)}")

    
    def attach_text(self, text):
        try:
            email_text = MIMEText(text, 'plain')
            self.email_message.attach(email_text)
        except Exception as e:
            raise Exception(f"Eroor in parameters: {str(e)}")


    def attach_html(self, html):
        try:
            email_html = MIMEText(html, 'html', 'utf-8')
            self.email_message.attach(email_html)
        except Exception as e:
            raise Exception(f"Eroor in parameters: {str(e)}")


    def attach_image(self, image_path, email_emage_name = None):
        try:
            image_file = open(image_path, 'rb')
            email_image = MIMEImage(image_file.read())
            image_file.close()

            # name extraction code here
            email_emage_name = "image"

            email_image.add_header('Content-Disposition', 'attachment', filename = email_emage_name)
            email_image.add_header('X-Attachment-Id', f'{self.image_attachement_id_counter}')
            email_image.add_header('Content-ID', f'<{self.image_attachement_id_counter}>')

            self.image_attachement_id_counter += 1

            self.email_message.attach(email_image)
        except Exception as e:
            raise Exception(f"Eroor with image attachement: {str(e)}")


    def send_message(self, subject, to_emails, is_urgent = False, show_smtp_debug = False):
            if isinstance(to_emails, str):
                to_emails = [to_emails]

            self.email_message.add_header('To', ', '.join(to_emails))
            self.email_message.add_header('From', self.email_sender)
            self.email_message.add_header('Subject', subject)

            if is_urgent:
                self.email_message.add_header('X-Priority', '1')
            
            try:
                smtp_server = SMTP_SSL(self.smtp_host, port=self.smtp_port)
            except:
                raise Exception("Error with smtp server configuration")

            if show_smtp_debug:
                smtp_server.set_debuglevel(1)

            try:
                smtp_server.ehlo()
            except:
                raise Exception("Error in handshake with smtp server")

            try:
               smtp_server.login(self.email_sender, self.email_password)
            except:
                raise Exception("Error with login operation")
            
            try:
                smtp_server.sendmail(self.email_sender, to_emails, self.email_message.as_bytes())
                smtp_server.quit()
            except:
                raise Exception("Error when sending mail")
