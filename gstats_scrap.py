def gstats(dept,code,year) :
	import httplib
	from string import split, replace, find
	conn = httplib.HTTPConnection("asc.iitb.ac.in")
	#dept, code, year = query.split()
	out = ""
	offered = 0
	for sem in range(1,3) :
		url = "/academic/Grading/statistics/gradstatforcrse.jsp?year=%s&semester=%d&txtcrsecode=%s+%s" % (year, sem, dept, code)
		conn.request("GET", url)
		resp = conn.getresponse()
		data = resp.read()
		lines = data.split('\n')
		for line in lines :
			semflag = find(line, "NOT</font> offered in this semester")
			if semflag > 0 :
				break
		if semflag < 0 :
			offered = 1
			out += "Grading statistics of %s %s for year %s sem %d\n" % (dept, code, year, sem)
			grades = ['AA', 'AB', 'AP', 'BB', 'BC', 'CC', 'CD', 'DD', 'FR', 'II', 'XX', 'AU']
			i = 0
			flag = 0
			for i in range(0,12) :	
				sub = "<td><b>%s </b></td>" % (grades[i])	
				for line in lines :
					if flag == 1 :
						line = line.replace('<td><b>', '')
						line = line.replace('</b></td>', '')
						gcount = int(line)
						out += '%s %d\n' % (grades[i], gcount)
						flag = 0
						break
					elif find(line, sub) > 0 :
						flag = 1
	if offered == 0 :
		return "The course %s %s was not offered in year %s" % (dept, code, year)
	else :
		return out
if __name__ == "__main__" :
	print gstats('CS 191 2010')
