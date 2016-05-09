#! /usr/bin/python
import cgitb; cgitb.enable() #to handle errors
import time,copy,os, glob, sys, stat ,re  #glob for wild character usage
from os.path import join
import update,spell

update.update_index()		#check for latest modification in text files and creates index --this part is to be checked...hope it works fine..but still..

#-----------------------------------------------
class info:						#obj of this class stores word and its filename
	def __init__(self):
		self.word=''
		self.array={}
	def dictionary(self,word,file_info):
		self.word=word
		p=str(file_info).split()
		
		for y in p:
			filename=y.split(":")[0]
			self.array[filename]=y.split(":")[1]
			
	def makeclear(self):
		self.word=''
		array={}


#-------------------------search in upper level index


S=info()					#temporary object to store word and its file_name
records=[]					#records holds all objects corresponding to each word and file_name


#input: querry string; output filenames and corresponding word frequency  ------------------


def index_search(query):
	wrong_words=[]		
	fz=open("index.txt",'r')
	split_query=str(query).split()	
	for x in split_query:
		found=0
		fz.seek(0)
		for lines in fz:
			#print lines.strip().split("=>")[0].strip()
			if lines.strip().split("=>")[0].strip()==x:
				temp=lines.strip().split("=>")			
				filenames=temp[1].strip()
				#print filenames
				S.dictionary(x,filenames)
				A=copy.deepcopy(S)	#create copy of word object to be used for storage			
				records.append(A)
				S.makeclear()
				found=1
				break		
		if found==0:
			wrong_words.append(x);				

	return wrong_words


def normal_srch(query):
	start_time=time.time()				
	wrong_words=index_search(query)
	split_query=str(query).split()
	corrected_word=""
	flag=0					#if wrong_words is not empty then generate corrected string
	if wrong_words:
		
		for x in split_query:
			if x in wrong_words:
				corrected_word = corrected_word + " " + spell.correct(x)				
			else:
				corrected_word=corrected_word + " " + x
		
		final_result=index_search(corrected_word)
		flag=1

	query_time=time.time()-start_time
	
	if wrong_words and not final_result:
		print "Did you mean... "
		for x in corrected_word.split():
			
			if x in split_query:
				print "%s"%x
			else:
				print "<font color=blue><i>%s</i></font>"%x
	
	still_words_remaining = not(len(wrong_words) == len(split_query))
	
	if not wrong_words or not final_result or still_words_remaining:
		if flag==1 :					##case when input string has been corrected..
			evaluate(corrected_word)
		else:
			evaluate(query)
		print "<br>Your search query took <b><font color=blue>%s</font></b> seconds.<br><hr>"%query_time
		print_results()
		
	else:
		print "<br>Your search <b>%s</b> did not match any document"%(query)		
				



#----------------------------evaluate------------------------

possible_files={}			#dictionary to store filenames as key and its score as value
dict_file_matchline={}			#dict key filename -> relevant line list

#--------------input: querry string pointer. output: updated possible_files dict. having filenames and corresponding scores
def evaluate(*string):
		
	for word in records:
		for key in word.array.keys():
			possible_files[key]=int		#possible_files contains all filenames containing atleast one of the word
	
	for x in possible_files.keys():
		f=open('./files/' + x)
		count=0	
		for word in records:
			if word.array.has_key(x):
				count+=int(word.array[x])		
		possible_files[x]=count				#assigned scores to each file
		found_complete_string = False
		
		#recreate the search string from records
		search_string = ''
		
		for word_data in records:
			search_string = search_string + word_data.word + ' '
			
		search_string.strip() #remove the terminal space due to concatenation
		
		dict_file_matchline[x] = []
		
		for line in f:
			#for strings that get a perfect match
			#store the nearby content to display
			#content delimited by 'period' character
			if re.search(search_string,line,re.IGNORECASE)!=None:
				#split line by delimiter
				list_split_line = line.split('.',re.IGNORECASE)
				#if the split_line contains string
				for split_line in list_split_line:
					split_line=split_line.lower()							
					if re.search(search_string ,split_line,re.IGNORECASE):
						#split at search_string
					
						parts_of_split_line = split_line.split(search_string,re.IGNORECASE)
						#make the search_string bold -- insert <b> tags
						BOLD_SEARCH_STRING = " <b>" + search_string + "</b> "
						bold_line = ''
						iter_no = 0
						for part in parts_of_split_line:
							if iter_no != 0:							
								bold_line = bold_line + BOLD_SEARCH_STRING +part
							else:
								bold_line = part #for the first part exception
							iter_no = iter_no + 1

							
						dict_file_matchline[x].append(bold_line)
						found_complete_string = True
				
				if len(records) > 1 :#if more than 1 keywords
					possible_files[x]+=100
					
		
		#for those which didn't get a relevant complete match
		#do a single word search for each word
		if found_complete_string == False:
			f.seek(0)
			for line in f:
				list_split_line = line.split('.')
				for split_line in list_split_line:
					#search line for all words
					for word_data in records:
						if re.search(word_data.word ,split_line):
													#split at search_string
							parts_of_split_line = split_line.split(word_data.word)
							#make the search_string bold -- insert <b> tags
							BOLD_SEARCH_STRING = " <b>" + word_data.word + "</b> "
							bold_line = ''
							iter_no = 0
							for part in parts_of_split_line:
								if iter_no != 0:							
									bold_line = bold_line + BOLD_SEARCH_STRING +part
								else:
									bold_line = part #for the first part exception
								iter_no = iter_no + 1

							dict_file_matchline[x].append(bold_line)
							break

		
		
		
		f.close()
		
					
	f_history = open('history' , 'a')
	f_history.write('\n' + search_string)
	f_history.close()
	
			

		
				
		
		
#-----------------------------------------print			display search results



def print_results():
	
	header_data_hidden = ''' <link rel="stylesheet" type="text/css" href="../../static/cssverticalmenu.css" />

<script type="text/javascript" src="../../static/cssverticalmenu.js">

</script>
 '''
	header_data_open = ''' <link rel="stylesheet" type="text/css" href="../../static/normal.css" />


</script>
 '''

	results=sorted(possible_files.items(), key=lambda(k,v):(v,k))
	results.reverse()

	print "<html>"
	
	
	
	print '''<body  bgcolor="#7f9f24" onLoad="createAutoComplete();">'''
	total_lines = 0
	for r in results:
		instances = dict_file_matchline[r[0]]
		total_lines = total_lines + len(instances)
		
	if total_lines < 10:
		print header_data_open
	else:
		print header_data_hidden
	
	print '''<ul id="verticalmenu" class="glossymenu">'''

	for r in results:
		print "	<li><a href='%(addr)s'> %(file_name)s  </a>" %{ "addr" : ("../../static/files/" + str(r[0])) , "file_name": str(r[0])  }
		instances = dict_file_matchline[r[0]]
		print "		<ul>"
		for instance in instances:
			print "			<li><a>" + instance + "</a></li>"
		print "		</ul>"
		print "		</li>"
			
	
	print '''</ul>'''
	print "<br> <br></body>"
		
		
	print "</html>"
			
	
#----------------------------- this function is yet to be implemented/removed.. strict_search feature means search only for exact string match	
def strict_srch(*querry):
	print querry


		

if __name__=='__main__':
	normal_srch('computer')


