#!/usr/bin/python

""" This classifier program will use the spamicity of each token of the message 
and then determine the classification of the email as spam/ham """


""" Usage : Enter the file in the command line argument """

import json
import sys
import email
from BeautifulSoup import BeautifulSoup
import re

def main():
	
	f = open(sys.argv[1])
	msg = parser.parse(f)
	f.close()
	text = msg.get_payload()
	try:
		text = text.lower()

	except AttributeError:
		
		for check in msg.get_payload():
			q = check['Content-Type']
			if check['Content-Transfer-Encoding']=='base64':
				print 'This program is not trained with base64 encoding . Hence it cannot classify'
				sys.exit(0)
		
		text = ' '
		for ex in msg.get_payload():
			try:
				text = text+ex.get_payload()

			except TypeError:
				print 'This program is facing difficulty in reading this mail....Terminating'
				sys.exit(0)

		text = text.lower()

	try:
		tokens = ' '.join(BeautifulSoup(text).text.split())
		
		temp_special = ' '.join(reg2.findall(tokens)) #extracting special characters 
		special_char = temp_special.split()
		tokens = reg.findall(tokens) + special_char 
	
	except TypeError:
		print 'SomeThing got messed up during regex'
		print ' Terminating .... '


if __name__=='__main__':

	parser = email.Parser.Parser()
	reg = re.compile('[a-z]+',re.IGNORECASE)
	reg2 = re.compile('\W+')
	json_data = open('spam_token_contribution.db')
	spam_prob = json.load(json_data)
	json_data.close()
	
	json_data = open('ham_token_contribution.db')
	ham_prob = json.load(json_data)
	json_data.close()

	main()


