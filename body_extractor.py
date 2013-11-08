#!/usr/bin/python

import mailbox
import os
import email
import re
from BeautifulSoup import BeautifulSoup
import json
import sys

p = email.Parser.Parser()
word_count = {}
reg = re.compile('[a-z]+',re.IGNORECASE)
reg2 = re.compile('\W+') #getting all the special characters
counter = 0 
directory = sys.argv[1]

path ='./'+directory+'/'
print path

for i in os.listdir(path):
	fp = open(path+i,'rb')
	msg = p.parse(fp)
	fp.close()
	text = msg.get_payload() #get the pay_load
	try:
		text = text.lower()
	except AttributeError:
		flag = 0
		for check in msg.get_payload(): #For all the mails that are base64 encoded ignore them
			q = check['Content-Type']
			if check['Content-Transfer-Encoding']=='base64':
				print 'base64 :',i
				flag = 1
				break
		if flag ==1 :
			continue


		text = ' '
		for ex in msg.get_payload():
			try:
				text = text+ex.get_payload()
				
			except TypeError:
				counter+=1
				print i,':',counter #check how many emails cannot be read	
				continue
			
		text = text.lower()	
	try:
		tokens = ' '.join(BeautifulSoup(text).text.split())
		temp_special = ' '.join(reg2.findall(tokens))
		special_char = temp_special.split()
		tokens = reg.findall(tokens) + special_char
		
	except TypeError:
		print 'Some shit happened in finding the regex'
		continue
			
	for words in tokens:
		if words not in word_count:
			word_count[words]=1
		else:
			word_count[words]+=1 # counting their occurences

for i,j in word_count.iteritems():
	if j>50:
		print i,j

if directory=='spam':
	with open('spam_dict.txt','w') as outfile:
		json.dump(word_count,outfile)
	
elif directory == 'easy_ham':
	with open('ham_dict.txt','w') as outfile:
		json.dump(word_count,outfile)

elif directory == 'spam_2':
	with open('more_spam_dict.txt','w') as outfile:
		json.dump(word_count,outfile)
#Bug : throw all the extra HTML tags
# convert all the words to lowercase
