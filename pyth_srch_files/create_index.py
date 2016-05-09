#! /usr/bin/python

import os,string,copy		#useful to imitate object
#import re		#not reqd. useful for re.search("str1","str2") and re.match("str1","str2")



class store:									#this class stores word and filename
	def __init__(self):
		self.word=""
		self.filename=[]
	def makeclear(self):
		self.word=""
		del self.filename[:]
#-----------------------------------------------

S=store()									
dictionary=[]									#final records to be written
word_processed=[]								#words indexed till now...
#----------------------------------------------------
#------------no input parameter. reads processed files(file1_processed stores "word:frequency" for that file) and combines all processed files to create index file 
def function():		
	file_list=os.listdir('./processed')			#get all processed files
	for i in range(0,len(file_list)-1):
		fo1=open('./processed/'+file_list[i])
				
		for lines in fo1:
			lines=lines.strip()
		        flag=1	
			if lines.split(":")[0] not in word_processed:
				S.word=lines.split(":")[0]				#time to store
				S.filename.append(file_list[i].replace('_processed','') + ":" + lines.split(":")[1] + " ")
										
				for j in range(i+1,len(file_list)):
					for a in open('./processed/' + file_list[j]):
						if lines.split(":")[0]==a.split(":")[0]:
				#			if flag==1:							
				#				flag=0	
							S.filename.append( file_list[j].replace('_processed','') + ":" + a.strip().split(":")[1] + " ")	
							break
				#if flag==0:				#create duplicates only if s has been modified
				A=copy.deepcopy(S)					
				dictionary.append(A)
#				print S.word
				word_processed.append(S.word)
				S.makeclear()

		fo1.close()
	write_to_file()

#----------------------------------------------------------------
#--function to write data in index file in particular format
def write_to_file():
	fout=open('index.txt',"w+")	#for upper level index
	for x in dictionary:
		fout.write(x.word + " => ")
		for t in x.filename:		
			fout.write(t)
		fout.write("\n")

	fout.close()					
							

#-------------------------------------------------------------------

if __name__=='__main__':
	function()

