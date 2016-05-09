#Desktop indexing/search utility

Written in Python

Scans text files in a given folder and maintains a flatfile index sensitive to updates. The results are displayed in decreasing order of relevance. JS based intuitive and helpful UI. Maintains history. Intelligent suggestions based on past events. The results shown contains specific lines extracted from the file so that user can check the context in which the keyword has been used.

###To install (on linux machine with say XAMPP server) 

	* copy pyth_srch_files folder to cgi-bin folder in your server (most probably at <xampp_directory/> )
	* copy static_files to htdocs folder in the same directory.
	* fire up your xampp server
	* GOTO http://localhost/cgi-bin/pyth_srch_files/gui
	* you might also want to access the location from remote location.
	* files that are indexed and searched are stored in pyth_srch_files/files