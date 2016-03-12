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


@main_blueprint.route('/', methods=['GET', 'POST'])
# @user_blueprint.route('/register')

def home():
    print request.form
    if request.method == 'POST':
         print "TEEEEEST"
    return render_template('main/home.html')


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")
