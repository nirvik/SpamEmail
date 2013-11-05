#!/usr/bin/python

import mailbox
import os
import email
import re

p = email.Parser.Parser()
word_count = {}



for i in os.listdir('./new/'):
	fp = open('./new/'+i,'rb')
	msg = p.parse(fp)
	fp.close()
	text = msg.get_payload() #get the pay_load
	
	try:
		reg = re.compile('[a-z]+',re.IGNORECASE)
		#line_separator_text = ' '.join(text.split('\n')) #split according to the 'next line'
		#tokens = line_separator_text.split(" ") # get all the words
		try:
			tokens = reg.findall(text)
		except TypeError:
			continue
		for words in tokens:
			if words not in word_count:
				word_count[words]=1
			else:
				word_count[words]+=1 # counting their occurences

	except AttributeError:
		print 'Oops small error...Fuck it and continue'
		continue

for i,j in word_count.iteritems():
	if j>50:
		print i,':',j

#Bug : throw all the extra HTML tags
# convert all the words to lowercase
