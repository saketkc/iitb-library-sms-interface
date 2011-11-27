import re
import urllib
import httplib2
from BeautifulSoup import BeautifulSoup
import getpass

def get_grades(username,password,semester):
	http = httplib2.Http()
	url = 'http://www.iitb.ac.in/asc/ldaplogin.jsp'   
	body = {'user': username, 'pass': password}
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
	#response = urlfetch.fetch(url, 'POST', headers=headers, body=urllib.urlencode(body))


	url_location = response['location']

	dispurl=url_location

	headers = {'Host': 'www.iitb.ac.in','User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1', 'Accept':'	text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-us,en;q=0.5', 'Accept-Encoding': 'gzip, deflate','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7','Connection':	'keep-alive','Referer':'http://www.iitb.ac.in/asc/','Cookie': response['set-cookie']}

	response, content = http.request(dispurl, 'POST', headers=headers, body=urllib.urlencode(body))
	scraped_output = BeautifulSoup(content)

	a=str(scraped_output).strip()
	b = a.split("Semesterwise Details")
	c = b[1].split("Year/Semeser")
	d = c[-1].split("Fee Details")
	c[-1] = d[0]


	re_for_semester = re.compile("<td>.*<\/td>")
	all_entries = [[]]*len(c)

	for i in range(1,len(c)):
		all_entries[i-1].append(re_for_semester.findall(c[i]))


	for i in range(len(all_entries[0])):
		for j in range(len(all_entries[0][i])):
			all_entries[0][i][j]= all_entries[0][i][j].strip('<td></')

	grades =''
	count =0

	for i in range(len(all_entries[0][semester-1])):
		if i%5 ==0 or i%5 ==1 or i%5 ==3:
			grades+=all_entries[0][semester-1][i] + " "
			count+=1
			if count==3:
				grades+= '\n'
				count = 0

	return grades

print get_grades("saket.Kumar","thisisit1314.",2)
