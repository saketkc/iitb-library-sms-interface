from course_info import course_info
def courses(dept_code,course_code) :
	import httplib
	import httplib2
	import urllib
	from BeautifulSoup import BeautifulSoup
	from string import split, replace, find
	conn = httplib.HTTPConnection("asc.iitb.ac.in")
	#dept, code, year = query.split()
	out = ""
	offered = 0
	http = httplib2.Http()
        url = 'http://asc.iitb.ac.in/academic/commjsp/ldaplogin.jsp'
        body = {'user': 'saket.kumar', 'pass': 'thisisit1314.'}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
        url_location = response['location']
        splitted=url_location.split("&")
        roll_no=splitted[1].split("=")[1]
        dispurl='http://asc.iitb.ac.in/academic/utility/RunningCourses.jsp?deptcd='+dept_code+'&year=2012&semester=2'
        headers = {'Host': 'asc.iitb.ac.in','User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-us,en;q=0.5', 'Accept-Encoding': 'gzip, deflate','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7','Connection':    'keep-alive','Referer':dispurl,'Cookie': response['set-cookie']}
        #url ='http://libsuite.library.iitb.ac.in/iitlibdata/webopac8/l_renew.php?fromASC=Y&m_mem_id='+roll_no+'&m_location_cd=1'
        response, content = http.request(dispurl, 'GET', headers=headers)

	soup =  BeautifulSoup(content)
	#print soup
	table = soup.find('table')
	rows = table.findAll('tr')
	returnpara ="Course you entered was not found. The running courses are :\n"
	for row in rows:
		columns = row.findAll('td',{"bgcolor":"white","align":"left"})
		try:
			course_name = columns[1].a.string.replace(" ","")
			#print course_name
			if course_name==dept_code+course_code:
				#print "Yo"
				course_infor = course_info(dept_code+" "+course_code)
				return "*Course:* "+columns[1].a.string+":"+columns[2].string+"\n*Instructor:* "+columns[3].string+"\n*Slot:* "+columns[5].string.replace("&nbsp;","")+"\n*Description:* "+course_infor
			returnpara += str(columns[1].a.string)  + " : " + str(columns[2].string) +"\n"
		except:
			a=1
	return returnpara
if __name__ == "__main__" :
	print courses('AE','152')
