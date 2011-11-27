def moodle_updates(username,password):
	
	import urllib, urllib2, cookielib, mechanize, os, re, getpass
	from BeautifulSoup import BeautifulSoup
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	login_data = urllib.urlencode({'username':username, 'password': password })
	opener.open('http://moodle.iitb.ac.in/login/index.php', login_data)
	returnvalue=""
	url=opener.open('http://moodle.iitb.ac.in')
	url=url.read()
	courses=re.compile('<a title="Click to enter this course" href="(.*)')
	list=courses.findall(str(url))
	list[0]='http'+list[0]
	for i in range(len(list)):
		course_code= list[i].split("\">")[0].split("=")[1]
		course_name= list[i].split("</a>")[0].split("\">")[1]
		course_url='http://moodle.iitb.ac.in/course/view.php?id=' + course_code
		url_dump=opener.open(course_url)
			
		html=url_dump.read()
		html1=html.split('Activity since')
		html2=html1[1].split('div class="bb"')
		html3=html2[0].split('</a>')
		html3[1].strip('</div>')
		match = re.search('class="message".*?>(.*?)<', html3[1])
		if match:
			#print course_name
			#print match.group(1)
			#print ""
			returnvalue += str(course_name)+str(match.group(1))
		return returnvalue
		
		

