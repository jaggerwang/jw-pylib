import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re


def is_email_address(email):
    return bool(re.match(r'^.+@[^.].*\.[a-z]{2,10}$', email, re.IGNORECASE))


def send_email(subject, text, to, from_, html=None, host="localhost",
               port=25, username=None, password=None, tls=False):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['To'] = to
    msg['From'] = from_
    msg.attach(MIMEText(text, "plain"))
    if html is not None:
        msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(host, port) as smtp:
        if tls:
            smtp.starttls()
        if username and password:
            smtp.login(username, password)
        smtp.sendmail(from_, to, msg.as_string())


def send_email_by_mailgun(api_base_url, api_key, subject, text, to, from_,
                          html=None, cc=None, bcc=None, attachment=None,
                          inline=None):
    import requests
    from requests.auth import HTTPBasicAuth

    url = "{}/messages".format(api_base_url)
    auth = HTTPBasicAuth('api', api_key)
    data = {
        'subject': subject,
        'text': text,
        'to': (','.join(to) if isinstance(to, tuple) else to),
        'from': from_,
        'html': html,
        'cc': (','.join(cc) if isinstance(cc, tuple) else cc),
        'bcc': (','.join(bcc) if isinstance(bcc, tuple) else bcc)
    }
    data = {k: v for k, v in data.items() if v is not None}

    files = {}
    if attachment is not None:
        for i, v in enumerate(attachment):
            if isinstance(v, str):
                v = open(v, 'rb')
            files['attachment[{}]'.format(i)] = v
    if inline is not None:
        for i, v in enumerate(inline):
            if isinstance(v, str):
                v = open(v, 'rb')
            files['inline[{}]'.format(i)] = v
    files = files or None

    r = requests.post(url, auth=auth, data=data, files=files)
    return r.json()
