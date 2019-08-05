import smtplib

carriers = {
	'att':    '@mms.att.net',
	'tmobile':' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com'
}

def send_sms(destination_number, provider, gmail_auth_login, gmail_auth_pass, message):
    to_number = destination_number + carriers[provider]
    auth = (gmail_auth_login, gmail_auth_pass)

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    headers = ['From: {}'.format(gmail_auth_login), 'Subject: {}'.format("CryptoPuller Notification"), 'To: {}'.format(destination_number)]
    msg_body = '\r'.join(headers) + '\r\n\r\n' + '\n\n' + message

    # Send text message through SMS gateway of destination number
    server.sendmail(auth[0], to_number, msg_body)