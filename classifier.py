#!/usr/bin/python

""" This classifier program will use the spamicity of each token of the message 
and then determine the classification of the email as spam/ham """


""" Usage : Enter the file in the command line argument """

import json
import sys
import email
from BeautifulSoup import BeautifulSoup
import re
import operator  #sorting dict accoring to the spamicity


def fun(x):
	return 1.0-x

def main():
	
	spamicity= {}

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
		
	#	temp_special = ' '.join(reg2.findall(tokens)) #extracting special characters 
	#	special_char = temp_special.split()
		tokens = reg.findall(tokens) #+ special_char 
	
	except TypeError:
		print 'SomeThing got messed up during regex'
		print ' Terminating .... '
		sys.exit(0)
	
	
	for words in tokens:
		
		
		if words not in ham_prob and words not in spam_prob:
			spamicity[words]=0.4
			continue

		if words not in combined_spam and ham[words]<=5:
			spamicity[words]=0.4
			continue

		if words not in ham and combined_spam[words]<=5:
			spamicity[words]=0.4
			continue
		if words in ham and words in combined_spam:
			if ham[words]<=5 and combined_spam[words]<=5:
				spamicity[words]= 0.4
				continue
		
		if words not in spam_prob:
			spam_prob[words]=0.0

		if words not in ham_prob:
			ham_prob[words]=0.0
		

		spamicity[words] = spam_prob[words]/(spam_prob[words]+ham_prob[words])
	
	for i,j in spamicity.iteritems():
		print i,':',j
	
	print 'Done tokenzing and determing the spamicity of tokens'
	
	best_tokens = []
	for i in spamicity.itervalues():
		best_tokens.append(i)

	best_tokens = sorted(best_tokens,reverse = True)[:-10] #taking the top 15 spamicity words 

	not_best = map(fun,best_tokens) #gettin a list of [1-x1,1-x2,1-x3,...]
	print ' Best ' + str(best_tokens)	
	print 'Not Best ' + str(not_best)


	num = reduce(lambda x, y:x*y,best_tokens)
	den = reduce(lambda x, y:x*y,best_tokens) + reduce(lambda x,y:x*y,not_best)
	result = num/den
	if result>0.5:
		print 'Its a Spam'
	else:
		print 'its a Ham'

	print 'The ans is result of {0}/{1} = {2}'.format(num,den,result)


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

	json_data = open('ham_dict.txt')
	ham = json.load(json_data)
	json_data.close()
	json_data = open('more_spam_dict.txt')
	spam2 = json.load(json_data)
	json_data.close()
	json_data = open('spam_dict.txt')
	spam = json.load(json_data)
	json_data.close()

	combined_spam = dict(spam.items() + spam2.items())

	main()
