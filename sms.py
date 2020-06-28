import os
import smtplib

carriers = {
	'att':    '@mms.att.net',
	'tmobile':' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com'
}

TO_NUMBER = '3603918051'
CELL_CARRIER = 'verizon'
GMAIL_ADDRESS = 'fractaldev2020@gmail.com'
GMAIL_PASS = 'FDUWXGGEW'

def send(message):
	# Replace the number with your own, or consider using an argument\dict for multiple people.
	to_number_address = '{}{}'.format(TO_NUMBER, carriers[CELL_CARRIER])
	auth = (GMAIL_ADDRESS, GMAIL_PASS)

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()
	server.login(auth[0], auth[1])

	print("Sending message...")

	# Send text message through SMS gateway of destination number
	server.sendmail( auth[0], to_number_address, message)

	print("Message sent.")