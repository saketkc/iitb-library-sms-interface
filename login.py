import re
import urllib
import httplib2
from BeautifulSoup import BeautifulSoup

http = httplib2.Http()

url = 'http://asc.iitb.ac.in/academic/commjsp/ldaplogin.jsp'   
body = {'user': 'saket.kumar', 'pass': 'thisisit1314.'}
headers = {'Content-type': 'application/x-www-form-urlencoded'}
response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
#print response['set-cookie']
headers = {'Host': 'asc.iitb.ac.in','User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-us,en;q=0.5', 'Accept-Encoding': 'gzip, deflate','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7','Connection':	'keep-alive', 'Referer':'	http://asc.iitb.ac.in/academic/commjsp/displayURL.jsp?username=saket.kumar&code=09D02007&emptype=S','Cookie': response['set-cookie']}

#print headers
#url="http://asc.iitb.ac.in/academic/utility/middlecas.jsp?loginCode=09D02007&loginnumber=09D02007&loginName=Saket%20Kumar%20Choudhary&Home=ascwebsite"
#url="http://asc.iitb.ac.in/academic/utility/middlecas.jsp?loginCode=09D02007&loginnumber=09D02007&loginName=Saket%20Kumar%20Choudhary&Home=ascwebsite"
#url="http://libsuite.library.iitb.ac.in/iitlibdata/webopac8/opac_ldap.php?nameid=09D02007"
url = 'http://libsuite.library.iitb.ac.in/iitlibdata/webopac8/l_renew.php?fromASC=Y&m_mem_id=09D02007&m_location_cd=1'   
response, content = http.request(url, 'POST', headers=headers)
#print response
scraped_output = BeautifulSoup(content)
#print scraped_output
#comment = commentSoup.find(text=re.compile("nice"))
#print scraped_output
p= re.compile("<font face=\"Arial\" size=\"2\">.*<\/font>")#\([A-Z&]\S*\s*\)+<\/font>")
#p= re.compile("<font face=\"Arial\" size=\"2\" color=\"black\">\d\d\/\d\d\/\d\d\d\d<\/font>")
s= p.findall(content)
#s= scraped_output.findAll(text=re.compile("\d\d\/\d\d/\d\d\d\d")) 
#<font face="Arial" size="2" color="black">10/11/2011</font>
print s
#for t in s:
   #print t
#ns= scraped_output.findAll("table",border=0)
#for t in s:
 #   print t
  #  print "#############################"
