#! /usr/bin/python
print "Content-type: text/html"
print ""

print "<h1><font color=blue>HISTORY:</font></h1><br>"
print "<body bgcolor=#7f9f24>"
print "<form action='gui'>"
print "<input type=submit name=back value='back'>"
print "</form>"

import os
f_history = open(os.path.abspath('history') , 'r')

if f_history == None:
	print "error - cannot open file" 
list_history = f_history.readlines()
list_history.reverse()
if len(list_history) < 5:
	print '''<ul>'''
	for search_entry in list_history:
		if search_entry.strip() != '':
			print '''<li> ''' + search_entry + '''</li>'''
	print '</ul>'
else:
	for i in range(5):
		print '''<ul>'''
		if list_history[i].strip() != '':
			print '''<li> ''' + list_history[i] + '''</li>'''
		print '</ul>'
	
print "</body>"
