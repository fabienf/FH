# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, jsonify
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request,session
from extractor import *
from predict import *
import numpy as np
import json
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
enum = ["love", "haha", "yay", "wow", "sad", "angry"]
e = Extractor()


@main_blueprint.route('/', methods=['GET', 'POST'])
# @user_blueprint.route('/register')

def home():
    print request.form
    vapi = None
    ll = None
    if request.method == 'POST':
         i = request.form["img"]
         l = request.form["link"]
         ll = request.form["l2"]
         print ll, "222333ljkj"
         user_input = {
             "article_link": l,
             "image_link": i
         }
        #  bhgjjjjjjjjjjj
        #  print i,l
        #  bbbbbb
        #  b = e.user_extract(user_input)
         b , t = predict(user_input["article_link"], user_input["image_link"])
         vapi = vap.get_json(request.form["img"])
        #  bbbbbbbbbb
         print vapi
        #  print vapi["scores"], "##########"
         x = list()
         for j in json.loads(vapi):
              print j,"~~~~~~~~~~####"
              x .append(j["scores"].keys()[np.argmax(j["scores"].values())]  )

         vap.dat = {"img":vapi,"wat" : enum[np.argmax(b) ], "xd": x, "tax": t}
        #  print vapi
    return render_template('main/home.html', vap= vapi, l2=ll)



@main_blueprint.route('/get_analysis')
def get_analysis():
    """
    route to hold data to display
    """
    print "TEST"
    x = None
    print vap.dat
    y = None
    f = None
    xd = None
    # print request.form
    if (vap.dat is  None or 'img' not in vap.dat):
        x = []
    else:
        x = vap.dat['img']
        y = vap.dat["wat"]
        f = vap.dat["tax"]
        xd = vap.dat["xd"]
    return jsonify(img=x, test='test', wat=y, tax=f,feels=xd)



@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")
