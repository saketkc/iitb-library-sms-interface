#!/usr/bin/python
from BeautifulSoup import BeautifulSoup
import urllib, urllib2, cookielib, re, os, shutil, MySQLdb, subprocess
login_url = {"2009":"http://moodle.iitb.ac.in/moodle2009/login/index.php","2011":"http://moodle.iitb.ac.in/moodle2011/login/index.php","2013":"http://moodle.iitb.ac.in/login/index.php"}
resource_url = {"2009":"http://moodle.iitb.ac.in/moodle2009/mod/resource/index.php?id=","2011":"http://moodle.iitb.ac.in/moodle2011/mod/resource/index.php?id=","2013":"http://moodle.iitb.ac.in/mod/resource/index.php?id="}
resource_view_url = {"2009":"http://moodle.iitb.ac.in/moodle2009/mod/resource/","2011":"http://moodle.iitb.ac.in/moodle2011/mod/resource/","2013":"http://moodle.iitb.ac.in/mod/resource/"}
course_url={"2009":"http://moodle.iitb.ac.in/moodle2009/course/view.php?id=","2011":"http://moodle.iitb.ac.in/moodle2011/course/view.php?id=","2013":"http://moodle.iitb.ac.in/course/view.php?id="}
base_url = {"2009":"http://moodle.iitb.ac.in/moodle2009","2011":"http://moodle.iitb.ac.in/moodle2011","2013":"http://moodle.iitb.ac.in/"}
def moodle_updates(username,password):

    proxy_support=urllib2.ProxyHandler({})
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), proxy_support)
    login_data = urllib.urlencode({'username':username, 'password': password })
    conn = MySQLdb.connect(host= "localhost", user=user, passwd=pwd, db="moodle_courses")
    cursor = conn.cursor()

    for year in login_url:
      print year
      opener.open(login_url[year], login_data)
      url=opener.open(base_url[year])
      url=url.read()
      courses=re.compile('<a title="Click to enter this course" href="(.*)')
      list=courses.findall(str(url))
      for i in range(len(list)):
        course_code= list[i].split("\">")[0].split("=")[1]
        course_name= list[i].split("</a>")[0].split("\">")[1].split(':')[0].rstrip()
        print course_name
        c_url=course_url[year]+course_code
        r_url=resource_url[year]+course_code
        try:
          cursor.execute("SELECT * FROM courses WHERE year = %s and course = %s",(year,c_url))
          rows = cursor.fetchall()
          count = len(rows)
          if count<1:
            should_download=True

            try:
              print "inserting"
              cursor.execute("INSERT INTO courses(year,course) VALUES(%s,%s)",(year,c_url))
              conn.commit()
            except:
              print "rollback"
              conn.rollback()
          else:
            should_download = False
        except:
          print "error with db"
        if should_download:
          cursor.execute("SELECT * FROM course_mappings WHERE course_url=%s",(c_url))
          result = cursor.fetchone()
          try:
            course_sem = result[2]
          except:
            course_sem=''

          
