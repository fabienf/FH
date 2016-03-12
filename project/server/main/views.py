# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, jsonify
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request,session


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################



########### Python 2 #############
import httplib as httplib, urllib as urllib, base64
import json

# Soz for this blasphemy :'( its the need for speed #YouOnlyFacebookOnce

class VisionAPI:
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '4211f4e020b74e23b73be45672d4f2c7',
    }

    body = {"URL": None}
    dat = None

    def __init__(self):
        pass

    def get_json(self, url):
        self.body["URL"] = url
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/emotion/v1.0/recognize", json.dumps(self.body) , self.headers)
        response = conn.getresponse()#
        data = response.read()
        # print(data)
        conn.close()
        return data


vap = VisionAPI()


@main_blueprint.route('/', methods=['GET', 'POST'])
# @user_blueprint.route('/register')

def home():
    print request.form
    vapi = None
    if request.method == 'POST':

         vapi = vap.get_json(request.form["img"])
         vap.dat = {"img":vapi}
        #  print vapi
    return render_template('main/home.html', vap= vapi)



@main_blueprint.route('/get_analysis')
def get_analysis():
    """
    route to hold data to display
    """
    print "TEST"
    x = None
    print vap.dat
    # print request.form
    if 'img' not in vap.dat:
        x = []
    else:
        x = vap.dat['img']
    return jsonify(img=x, test='test')



@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")
