# import the necessary components first
import smtplib
import textwrap
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
port = 2525
smtp_server = "smtp.mailtrap.io"
login = "3c45f4d987a262" # paste your login generated by Mailtrap
password = "bccfe6d5c5d5bf" # paste your password generated by Mailtrap


def send_email(sender, receiver):

    message = MIMEMultipart("alternative")
    message["Subject"] = "Activate your account"
    message["From"] = sender
    message["To"] = receiver
    # write the plain text part
    text = """\
    Hi,
    Check out the new post on the Mailtrap blog:
    SMTP Server for Testing: Cloud-based or Local?
    /blog/2018/09/27/cloud-or-local-smtp-server/
    Feel free to let us know what content would be useful for you!"""
    # write the HTML part
    html = """\
    <html>
    <body>
        <p>Hi,<br>
        Check out the new post on the Mailtrap blog:</p>
        <p><a href="/blog/2018/09/27/cloud-or-local-smtp-server">SMTP Server for Testing: Cloud-based or Local?</a></p>
        <p> Feel free to <strong>let us</strong> know what content would be useful for you!</p>
    </body>
    </html>
    """
    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    part1 = MIMEText(textwrap.dedent(text), "plain")
    part2 = MIMEText(textwrap.dedent(html), "html")
    message.attach(part1)
    message.attach(part2)
    # send your email
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login(login, password)
        server.sendmail(
            sender, receiver, message.as_string()
        )
    print('Sent') 

send_email("jobfinder@example.com","applicant@example.com")
