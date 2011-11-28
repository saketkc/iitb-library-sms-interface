import httplib2
import urllib
from BeautifulSoup import BeautifulSoup
import re


def library_info(username,password):
	http = httplib2.Http()
	url = 'http://asc.iitb.ac.in/academic/commjsp/ldaplogin.jsp'   
	body = {'user': username, 'pass': password}
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
	url_location = response['location']
	splitted=url_location.split("&")
	roll_no=splitted[1].split("=")[1]
	dispurl='http://asc.iitb.ac.in/academic/commjsp/displayURL.jsp?username='+username+'&code='+roll_no+'&emptype=S'
	headers = {'Host': 'asc.iitb.ac.in','User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-us,en;q=0.5', 'Accept-Encoding': 'gzip, deflate','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7','Connection':	'keep-alive','Referer':dispurl,'Cookie': response['set-cookie']}
	url ='http://libsuite.library.iitb.ac.in/iitlibdata/webopac8/l_renew.php?fromASC=Y&m_mem_id='+roll_no+'&m_location_cd=1'   
	response, content = http.request(url, 'POST', headers=headers)
	scraped_output = BeautifulSoup(content)
	all_contents=scraped_output.findAll('font',{"face":"Arial", "size":"2","color":"black"})
	regexp = re.compile("<font face=\"Arial\" size=\"2\">.*<\/font>")
	regexp_dates = re.compile("\d\d\/\d\d\/\d\d\d\d")
	book_names= regexp.findall(str(all_contents))
	book_dates = regexp_dates.findall(str(all_contents))
	for i in range(0,len(book_names)):
	    book_names[i]=book_names[i].replace("<font face=\"Arial\" size=\"2\">","")
	    book_names[i]=book_names[i].replace("</font>","")
	    book_names[i]=book_names[i].replace("<br>","")
	all_info=""
	for i in range(0,len(book_names)):
	    all_info += book_names[i] + "=>"  + book_dates[2*i+1] + "\n"
	return all_info

