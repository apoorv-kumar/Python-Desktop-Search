#! /usr/bin/python

import os, time, stat
from os.path import join


#data structures

records=[]	#to store words in form of class objects
temp=[]		#temporarily stores all diff. words.....
redundant=[]
rem=[',',';','.',':','-',']','[','?','/','\\','|',')','(','#','&','!','9','8','7','6','5','4','3','2','1','0',"\"",'\'']	# to be removed.....
#---------------------------------------------

#get list of all redundant words ----------reads redundant words from file redundant.txt and add them to redundant[]
def get_redund():
	
	fo=open(os.path.abspath('redundant.txt'),'r+')
	for lines in fo.readlines():
		for word in lines.strip().split(" "):
			redundant.append(word)
	fo.close()
#---------------------------------------

last_run=int				#latest file run time


#-----------input type: file1.txt output type: file1_processed.txt ------generates processed_file for file passed as parameter

def process_file(file):
	get_redund()				#call redundant data function
	fo=open(file,'r+')     # file object created  
	for lines in fo.readlines():	
		for word in lines.strip().lower().split(" "):		#strip function is used to remove new line chars read.		
					#convert words into lower case
			for t in rem:
				word=word.replace(t,'')		#removing ',',and other ...
			#print "hello" + word
			word.strip()
			if word !="":
				if check_word(word):
					pass
				else:
					store_word(word)
	fo.close()
	(filepath,filename)=os.path.split(file)
	fo=open(os.path.join(os.path.abspath('processed'),filename.split(".")[0] + "_processed" + ".txt"),'w+')	#appends name of file with _processed	
	for i in range(0,len(records)):
		fo.write(records[i].data + ":" + str(records[i].freq) + "\n")	#records written to file_processed ;int has to be converted in str..
	fo.close()
	#print file
	#print redundant
	del records[:]
	del temp[:]
	del redundant[:]
	last_run=time.time()	
 	fo=open('time.txt','w+')
	fo.write(str(last_run))
	fo.close()	
	
			
#-------------------------------------

# ------------check whether word is redundant or not
def check_word(word):
	if word in redundant:
		return True
	else:
		return False

#--------------------------------------

class word_freq:
	def __init__(self,word):
		self.data=word		#store word  ..dont forget to add self as prefix
		self.freq=1		#integer type to store freq
	
#---------------------------------------
#-----add object corresponding to each word(holding word and freq) to records[]
def store_word(word):
	if word in temp:
		i=temp.index(word)
		records[i].freq+=1
	else:
		x=word_freq(word)
		temp.append(word)
		records.append(x)

#------------------------------------------
if __name__=='__main__':
	process_file('./files/file3.txt')
			 
