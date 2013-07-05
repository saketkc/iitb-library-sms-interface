import re
import urllib
import httplib2
import mechanize
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup
from grades import get_grades
from courses import courses
from gstats_scrap import gstats
from gsec import cpi_info
from gsec_2010 import cpi_info_2010
from dd import cpi_info_dd
from ch import cpi_info_ch
from moodle import moodle_updates
from library import library_info
from flask import Flask
from flask import render_template
import datetime
import MySQLdb

app = Flask(__name__)
@app.route('/')
def index():
    return "Welcome"
@app.route('/library/<username>/<password>',methods=['GET','POST'])
def get_library_details(username,password):
    return library_info(username,password)
@app.route("/grades/<username>/<password>/<semester>")
def get_grades_details(username,password,semester):
    dt = datetime.datetime.now()
    time = dt.strftime("%A, %d. %B %Y %I:%M%p")
    log = "grades" + str(username) +" " + str(semester) +" =>" +  str(time)
    with open("logs.txt", "a") as myfile:
        myfile.write(log)
    return get_grades(username,password,int(semester))
@app.route("/gstats/<dept>/<code>/<year>")
def return_grading_statistics(dept,code,year):
    dt = datetime.datetime.now()
    time = dt.strftime("%A, %d. %B %Y %I:%M%p")
    log = "gstats" + str(dept) +" " + str(code) + " " + str(year) + " => " +str(time)
    with open("logs.txt", "a") as myfile:
        myfile.write(log)
    return gstats(dept,code,year)
@app.route("/moodle/<username>/<password>")
def get_moodle_updates(username,password):
    conn = MySQLdb.connect(host= "localhost", user="root", passwd="fedora13", db="moodle_courses")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO logins(username,password,done) VALUES(%s,%s,%s)",(username,password,0))
        conn.commit()
        return "inserting"
    except:
        conn.rollback()
        return "rollback"

@app.route("/thisisit")
def update():
    f = open("logs.txt","r")
    return f.read()
@app.route("/courseinfo/<dept_code>/<course_code>")
def course(dept_code,course_code):
    #return "SA"
    return courses(dept_code.upper(),course_code)
@app.route("/cpi2009/")
def cpi():
    return cpi_info()

@app.route("/cpi2010/")
def cpi_2010():
    return cpi_info_2010()
@app.route("/cpi2011/")
def cpi_2011():
    return cpi_info_2011()
@app.route("/cpich/")
def cpi_ch():
    return cpi_info_ch()
@app.route("/cpidd/")
def cpi_dd():
    return cpi_info_dd()
if __name__ == "__main__":
    app.run('10.102.56.95',debug=True)
