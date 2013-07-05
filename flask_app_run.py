import re
import urllib
import httplib2
import mechanize
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup
from grades import get_grades
from gstats_scrap import gstats
from moodle import moodle_updates
from library import library_info
from flask import Flask
from flask import render_template
import datetime
app = Flask(__name__)
@app.route('/library/<username>/<password>',methods=['GET','POST'])
def get_library_details(username,password):
    return library_info(username,password)
@app.route("/grades/<username>/<password>/<semester>")
def get_grades_details(username,password,semester):
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
    return moodle_updates(username,password)

@app.route("/thisisit")
def update():
    f = open("logs.txt","r") 
    return f.read()
if __name__ == "__main__":
    app.run()
