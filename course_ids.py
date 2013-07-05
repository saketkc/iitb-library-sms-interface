import urllib2, cookielib, urllib
from BeautifulSoup import BeautifulSoup
import MySQLdb
login_url = {"2009":"http://moodle.iitb.ac.in/moodle2009/login/index.php","2011":"http://moodle.iitb.ac.in/moodle2011/login/index.php","2013":"http://moodle.iitb.ac.in/login/index.php"}
resource_url = {"2009":"http://moodle.iitb.ac.in/moodle2009/mod/resource/index.php?id=","2011":"http://moodle.iitb.ac.in/moodle2011/mod/resource/index.php?id=","2013":"http://moodle.iitb.ac.in/mod/resource/index.php?id="}
resource_view_url = {"2009":"http://moodle.iitb.ac.in/moodle2009/mod/resource/","2011":"http://moodle.iitb.ac.in/moodle2011/mod/resource/","2013":"http://moodle.iitb.ac.in/mod/resource/"}
course_url={"2009":"http://moodle.iitb.ac.in/moodle2009/course/view.php?id=","2011":"http://moodle.iitb.ac.in/moodle2011/course/view.php?id=","2013":"http://moodle.iitb.ac.in/course/view.php?id="}
base_url = {"2009":"http://moodle.iitb.ac.in/moodle2009/course/category.php?id=","2011":"http://moodle.iitb.ac.in/moodle2011/course/category.php?id=","2013":"http://moodle.iitb.ac.in/course/category.php?id="}
username = "saket.kumar"
password = "whatsinaname."
proxy_support=urllib2.ProxyHandler({})
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), proxy_support)
login_data = urllib.urlencode({'username':username, 'password': password })
conn = MySQLdb.connect(host= "localhost", user="root", passwd="fedora13", db="moodle_courses")
cursor = conn.cursor()

for year in login_url:
    opener.open(login_url[year], login_data)
    #url=opener.open(base_url[year])
    #url=url.read()
    category_url = opener.open(base_url[year]+"1&perpage=9999")
    category_html = BeautifulSoup(category_url.read())
    select_category = category_html.find("select")
    options = select_category.findAll("option")
    for option in options[:-1]:
        value = option['value']
        print year
        string_sem = option.string
        try:
            sid = value.split("=")[1]
        except:
            sid = value
        print sid
        new_url = opener.open(base_url[year]+sid+"&perpage=9999")
        all_html = new_url.read()
        soup = BeautifulSoup(all_html)
        table  = soup.find("table",{"class":"generalbox boxaligncenter"})
        if table:
        #print table
            all_trs = table.findAll('tr')
            for tr in all_trs[1:]:
                course_name = tr.td.a.string
                course_id = tr.td.a['href'].split("=")[1]
                new_course_url = course_url[year]+course_id
                print string_sem,course_name,course_id
                try:
                    cursor.execute("INSERT INTO course_mappings(course_id,course_sem,course_name,course_url) VALUES (%s,%s,%s,%s)",(course_id,string_sem,course_name,new_course_url))
                    conn.commit()
                except:
                    conn.rollback()
                    print "RRRRRRRRRRROLLLLBACCK"


    #print select_category

