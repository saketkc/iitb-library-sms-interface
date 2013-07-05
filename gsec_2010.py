def cpi_info_2010() :
    import httplib
    import httplib2
    import urllib
    import csv
    reader = csv.reader(open("/var/www/flask_app/rolls.csv"),delimiter=',')
    roll_2011=[]
    roll_2010=[]
    roll_2009=[]


    for row in reader:
        if row[0]:
            roll_2011.append(row[0])
        if row[1]:
            roll_2010.append(row[1])
        if row[-1]:
            roll_2009.append(row[-1])
    #print row

    from BeautifulSoup import BeautifulSoup
    from string import split, replace, find
    conn = httplib.HTTPConnection("asc.iitb.ac.in")
    #dept, code, year = query.split()
    out = ""
    offered = 0
    http = httplib2.Http()
    url = 'http://asc.iitb.ac.in/academic/commjsp/ldaplogin.jsp'
    body = {'user': 'gsecaaug', 'pass': 'forepicaa@iitb'}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    responses, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
    url_location = responses['location']
    splitted=url_location.split("&")
    roll_no=splitted[1].split("=")[1]
    grandoutput = ""
    for roll in roll_2010:
        dispurl='http://asc.iitb.ac.in/academic/JSP/studentinfo/studentinfo.jsp?rollno='+str(roll)#http://asc.iitb.ac.in/academic/utility/RunningCourses.jsp?deptcd='+dept_code+'&year=2012&semester=2'
        headers = {'Host': 'asc.iitb.ac.in','User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-us,en;q=0.5', 'Accept-Encoding': 'gzip, deflate','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7','Connection':    'keep-alive','Referer':dispurl,'Cookie': responses['set-cookie']}
        #url ='http://libsuite.library.iitb.ac.in/iitlibdata/webopac8/l_renew.php?fromASC=Y&m_mem_id='+roll_no+'&m_location_cd=1'
       # print dispurl
        response, content = http.request(dispurl, 'GET', headers=headers)
        soup =  BeautifulSoup(content)
        table = soup.findAll('table',{"width":"100%"})[2]
        rows = table.findAll('tr')
        grandoutput = grandoutput+"<br/>Roll: "+roll
        #print rol
        for row in rows:
            try:
                tds = row.findAll('td')
                for td in tds[:4]:
                    grandoutput = grandoutput + td.string + ",\t"
                grandoutput = grandoutput+"<br/>"
            except:
                pass
        #print grandoutput
    return grandoutput

##	returnpara =""
#	return str(rows[-2].findAll('td')[-1].string)
if __name__ == "__main__" :
    print cpi_info()
