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
    conn = MySQLdb.connect(host= "localhost", user="root", passwd="fedora13", db="moodle_courses")
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

          print course_sem


          url_dump = opener.open(c_url)
          html = url_dump.read()
          soup = BeautifulSoup(html)
          discussion = soup.find('li',{"class":"activity forum"})
          if discussion:

            discussion_url=discussion.a['href']
            #print discussion_url.a['href']
            url = opener.open(discussion_url)
            html = url.read()
            soup = BeautifulSoup(html)
            table = soup.find("table",{"class":"forumheaderlist"})
            if table:

              trs = table.findAll("tr")
              for tr in trs[1:]:
                td = tr.find("tr")
                url = tr.td.a['href']
                url_dump = opener.open(url)
                soup = BeautifulSoup(url_dump.read())
                attachments = soup.findAll('div',{"class":"attachments"})
                folderlocation = "/var/www/flask_app/"+str(year)+"/"+str(course_name)+"/"
                if not  os.path.exists(folderlocation):
                  os.makedirs(folderlocation)
                for attachment in attachments:
                  try:
                    url = attachment.a['href']
                  except:
                    url=None
                  if url:
                    print url
                    html = opener.open(url).read()
                    filelocation = folderlocation +  url.split('/')[-1]
                    pdf = open(filelocation ,"wb")
                    pdf.write(html)
                    pdf.close()
          if r_url:
            try:
              url_dump=opener.open(r_url)
            except:
              url_dump = None
            if url_dump:
              html=url_dump.read()
              soup=BeautifulSoup(html)
              folderlocation = "/var/www/flask_app/"+str(year)+"/"+str(course_name)+"/"
              if not  os.path.exists(folderlocation):
                os.makedirs(folderlocation)
              try:
                table = soup.find('table',{"class":"generaltable boxaligncenter"})
                tr = table.find('tr')
              except:
                table = soup.find('table',{"class":"generaltable mod_index"})
                #tr=table.find('tr')
              if table:
                rows = table.findAll('tr')
                for row in rows:
                  tds = row.findAll('td')
                  for td in tds:
                    try:
                      new_link = td.a['href']
                    except:
                      new_link = None
                    if new_link:
                        new_url = resource_view_url[year] + new_link
                        try:
                          url_dump = opener.open(new_url)
                        except:
                          url_dump = None
                        if url_dump:

                          html = url_dump.read()
                          generated_url = url_dump.geturl()
                          if generated_url!=new_url and 'moodle' in generated_url:
                            filelocation = folderlocation +  generated_url.split('/')[-1]
                            try:
                              pdf = open(filelocation ,"wb")
                            except:
                              pdf = open(filelocation+generated_url,"wb")
                            pdf.write(html)
                            pdf.close()
                          else:
                            new_soup = BeautifulSoup(html)
                            try:
                              all_links = new_soup.findAll('object')
                            except:
                              new_table = new_soup.find('table',{"class":"files"})
                              new_trs = new_table.findAll('tr')
                              all_links =[]
                              for tr in new_trs:
                                all_links.append(tr.find('td').find('a')['href'])

                            for link in all_links:
                              url = link['data']
                              pdf_content = opener.open(url).read()
                              filelocation = folderlocation +  url.split('/')[-1]
                              pdf = open(filelocation,"wb")
                              pdf.write(pdf_content)
                              pdf.close()
          to_copy = "/var/www/flask_app/downloads/"+year+"/"+course_name+".zip"
          course_name_new = course_name.replace(" ","").replace("&amp;","").replace(";","").replace("&","")+"_"+course_sem.replace(" ","")

          filename = shutil.make_archive("/var/www/flask_app/downloads/"+year+"/"+course_name_new,"zip",folderlocation)
          print filename
          subprocess.call("fab --fabfile=/var/www/flask_app/fabfile.py copy:"+filename+","+year,shell=True)






#moodle_updates('saket.kumar','whatsinaname.')
#moodle_updates('ishan.shrivastava', 'gauss5$5$')

new_conn = MySQLdb.connect(host= "localhost", user="root", passwd="fedora13", db="moodle_courses")
new_cursor = new_conn.cursor()
new_cursor.execute("SELECT * from logins WHERE done = %s",(0))
rows=new_cursor.fetchall()
for row in rows:
  username = row[0]
  password = row[1]
  moodle_updates(username,password)
  print username
  new_cursor.execute("UPDATE logins SET done=%s WHERE username=%s;",(1,username))
  new_conn.commit()

