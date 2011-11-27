import re
import urllib
import httplib2
import mechanize
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup
from grades import get_grades
from gstats_scrap import gstats
from moodle import moodle_updates
from flask import Flask
from flask import render_template
def library_data(username,password):
	http = httplib2.Http()
	#username=raw_input("LDAP ID: ").strip()
	#password=raw_input("Password: ").strip()
	url = 'http://asc.iitb.ac.in/academic/commjsp/ldaplogin.jsp'   
	body = {'user': username, 'pass': password}
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
#print response['set-cookie']
	url_location = response['location']
	splitted=url_location.split("&")
	roll_no=splitted[1].split("=")[1]
	dispurl='http://asc.iitb.ac.in/academic/commjsp/displayURL.jsp?username='+username+'&code='+roll_no+'&emptype=S'
	headers = {'Host': 'asc.iitb.ac.in','User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-us,en;q=0.5', 'Accept-Encoding': 'gzip, deflate','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7','Connection':	'keep-alive','Referer':dispurl,'Cookie': response['set-cookie']}
	#print headers
	#url="http://asc.iitb.ac.in/academic/utility/middlecas.jsp?loginCode=09D02007&loginnumber=09D02007&loginName=Saket%20Kumar%20Choudhary&Home=ascwebsite"
	#url="http://asc.iitb.ac.in/academic/utility/middlecas.jsp?loginCode=09D02007&loginnumber=09D02007&loginName=Saket%20Kumar%20Choudhary&Home=ascwebsite"
	#url="http://libsuite.library.iitb.ac.in/iitlibdata/webopac8/opac_ldap.php?nameid=09D02007"
	url ='http://libsuite.library.iitb.ac.in/iitlibdata/webopac8/l_renew.php?fromASC=Y&m_mem_id='+roll_no+'&m_location_cd=1'   
	response, content = http.request(url, 'POST', headers=headers)
	scraped_output = BeautifulSoup(content)
	re_for_books = re.compile("<font face=\"Arial\" size=\"2\">.*<\/font>")#\([A-Z&]\S*\s*\)+<\/font>")
	re_for_fine =  re.compile("<font face=\"Arial\" size=\"2\" color=\"red\">.*<\/font>")
	re_for_dates = re.compile("\d\d\/\d\d\/\d\d\d\d")
	fine= re_for_fine.findall(content)
	print fine
	all_dates = scraped_output.findAll(text=re.compile("\d\d\/\d\d/\d\d\d\d"))# re_for_dates.findall(content)
	all_books = re_for_books.findall(content)
	for i in range(0,len(all_dates)):
	    all_dates[i]=all_dates[i].replace("<font color=\"blue\" size=\"1\">New Due Date will be = " , "")
	    all_dates[i]=all_dates[i].replace("</font>","")
	    all_dates[i]=all_dates[i].replace("<br>","")
	for i in range(0,len(all_books)):
	    all_books[i]=all_books[i].replace("<font face=\"Arial\" size=\"2\">","")
	    all_books[i]=all_books[i].replace("</font>","")
	all_info={'Book': ['Due_Date','New_Due_Date','Issue_Date']}
	returnvalues="Book:"
	for i in range (0,len(all_books)):
	    returnvalues+=all_books[i]+" "+all_dates[i]
	return returnvalues
	"""
	i = 0
	for book in all_books:
	    all_info[book]=[all_dates[i],all_dates[i+1],all_dates[i+2]]
	    i=i+1
	print "Book", all_info["Book"][0],all_info["Book"][1],all_info["Book"][2]

	for info in  all_info:
	    if info!="Book":
		print info,all_info[info][0] ,all_info[info][1], all_info[info][2]
		"""
app = Flask(__name__)
@app.route('/library/<username>/<password>',methods=['GET','POST'])
def get_library_details(username,password):
    #username = request.args.get('u','')
    #password = request.args.get('p','')
    #print username
    #print password
    
    return library_data(username,password)#"T"  #render_template('hello.html',name='Test')
@app.route("/grades/<username>/<password>/<semester>")
def get_grades_details(username,password,semester):
    return get_grades(username,password,int(semester))
@app.route("/gstats/<dept>/<code>/<year>")
def return_grading_statistics(dept,code,year):
    return gstats(dept,code,year)
@app.route("/moodle/<username>/<password>")
def get_moodle_updates(username,password):
    return moodle_updates(username,password)
if __name__ == "__main__":
    app.run('10.5.10.12',debug=True)
