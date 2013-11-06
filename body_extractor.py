#!/usr/bin/python

import mailbox
import os
import email
import re

p = email.Parser.Parser()
word_count = {}
reg = re.compile('[a-z]+',re.IGNORECASE)
counter = 0 
for i in os.listdir('./new/'):
	fp = open('./new/'+i,'rb')
	msg = p.parse(fp)
	fp.close()
	text = msg.get_payload() #get the pay_load
	try:
		text = text.lower()
	
	except AttributeError:
		flag = 0
		for check in msg.get_payload(): #For all the mails that are base64 encoded
			if check['Content-Transfer-Encoding']=='base64':
				print 'base64 :',i
				flag = 1
				break
		if flag ==1 :
			continue

		counter+=1
		print i,':',counter

		text = ' '
		for ex in msg.get_payload():
			try:
				text = text+ex.get_payload()
				print ex,'ERROR'
				
			except TypeError:
				#for more in ex:	
					#if TypeError:
					#	break
					#print more.get_payload()
				continue
			
		
	try:
		tokens = reg.findall(text)
	
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
		print i,':',j

#Bug : throw all the extra HTML tags
# convert all the words to lowercase
