from fabric.api import env
from fabric.operations import run, put

env.hosts = ["gymkhana.iitb.ac.in"]
env.user = "ugacademics"
env.password = "ug12345^&"
env.parallel = False
def copy(filelocation,year):
    location_on_server = "/home/ugacademics/public_html/resources/"+year+"/"
    run('mkdir -p '+location_on_server)

    put(filelocation,  location_on_server)

