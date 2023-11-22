from flask import Flask,jsonify, render_template,request
from flask_cors import CORS,cross_origin
from utils import gmail_send_message

import random
import string
import time


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

complete_helps = []

class CompleteHelp:
    def __init__(self,first_person_ip):
        self.first_person_ip = first_person_ip
        self.second_person_email_address = None
        self.second_person_ip = None
        self.email = None
        self.password = None
        self.completed = False

    def ask_for_help(self,second_person_email):
        self.second_person_email_address = second_person_email

        gmail_send_message("Someone wants you to help them fill out this form",
        f"<a href='http://127.0.0.1:5000/help-fill/{self.first_person_ip}'><button>Click Here</button></a>",
        self.second_person_email_address)

    def __repr__(self):
        return f"Object <{self.second_person_email_address} | {self.first_person_ip}>"

def generate_random_characters():
    return ''.join(random.choices(string.ascii_letters, k=16))
    
 
@app.route("/")
def index_view_function():
    return jsonify({
        'data':"Hey this is working"
    })


@app.route("/asktofill-onbehalf",methods=["POST"])
def handle_asktofill_onbehalf():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        askemail = request.form.get("askemail")

        complete_help = CompleteHelp(request.remote_addr)
        complete_help.ask_for_help(askemail)
        complete_helps.append(complete_help)

        return jsonify({
                'data':"Successfully sent email to fill form on  your behalf",
                'info_code':1,
                'askemail':askemail,
                'your ip':request.remote_addr
            })
        

@app.route("/help-fill/<first_person_ip>",methods=["GET","POST"])
def help_route(first_person_ip):
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        for help_object in complete_helps:
            if help_object.first_person_ip == first_person_ip:
                help_object.email = email
                help_object.password = password
                help_object.completed = True
                break

        return "<h1>Thanks for helping ! </h1>"

    return render_template("help_fill.html",request_from_ip=first_person_ip)


@app.route("/check-help-data")
def check_data_handler():
    for help_object in complete_helps:
        if help_object.completed and help_object.email and help_object.password and help_object.first_person_ip == request.remote_addr:
            complete_helps.remove(help_object)

            return jsonify({
                'data':"Got data filled by remote user",
                'info_code':1,
                'askemail':help_object.second_person_email_address,
                'your ip':request.remote_addr,
                'entered_email':help_object.email,
                'entered_password':help_object.password
            })

    return jsonify({
        'data':"Failed getting data filled by remote user",
        'info_code':-1,
        'your ip':request.remote_addr
    })


if __name__ == "__main__":
    app.run(debug=True)

