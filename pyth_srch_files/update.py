#! /usr/bin/python

import os,time, stat
import proces_file, create_index

#-----------compares time when index.txt was created and latest modification time of files if less than recreate index
def update_index():
	prev_update=open('time.txt').readline()		#get last proces_file run time
	flag=0					
	#prev_update=time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(file_stats[stat.ST_MTIME]))

	for x in os.listdir('./files'):
		#file2_stats=os.stat('./files/'+x)
		update_time=os.stat('./files/'+x)[stat.ST_MTIME]
		if update_time > float(prev_update):			##!!!!!!!!!!!!!!!!!!!!convert string to float for compare!!!!!!!!!!!!!!!!!!!
			flag=1			
			proces_file.process_file('./files/'+ x)
			#print "called"
			print flag
	if flag==1:
					#modify index if file_proces has been called
		create_index.function()

if __name__=='__main__':
	update_index()
	
