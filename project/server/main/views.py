# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint
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





@main_blueprint.route('/', methods=['GET', 'POST'])
# @user_blueprint.route('/register')

def home():
    print request.form
    if request.method == 'POST':
         vap = VisionAPI()
         print vap.get_json(request.form["img"])
    return render_template('main/home.html')


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")
