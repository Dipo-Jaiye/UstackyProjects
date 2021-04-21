from flask import Flask, render_template, url_for, request, redirect, flash, current_app
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
import datetime
from os import environ as env

load_dotenv()
app = Flask(__name__)
app.secret_key = env.get("SECRET_KEY")
app.config["MYSQL_DATABASE_HOST"] = env.get("DB_HOST")
app.config["MYSQL_DATABASE_DB"] = env.get("DB_NAME")
app.config["MYSQL_DATABASE_USER"] = env.get("DB_USER")
app.config["MYSQL_DATABASE_PASSWORD"] = env.get("DB_PASSWORD")
mysql = MySQL(app,cursorclass=DictCursor)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/student/new",methods=["GET","POST"])
def student_new():
    if request.method == "GET":
        return render_template("student_new.html")
    else:
        s_fname = request.form['fname']
        s_mname = request.form['mname']
        s_lname = request.form['lname']
        s_email = request.form['email']
        s_dob = request.form['dob']
        s_gndr = request.form['gndr']
        s_phone = request.form['phone']
        s_addr = request.form['address']
        s_state = request.form['state']
        s_lg = request.form['lg']
        s_kin = request.form['kin']
        s_score = request.form['score']
        s_image = request.files['image']
        if [s_addr,s_dob,s_email,s_fname,s_gndr,s_image,s_kin,s_lg,s_lname,s_mname,s_phone,s_score,s_state] == "":
            flash("Please enter a valid input",'danger')
            return redirect(url_for('student_new'))
        else:    
            conn = mysql.get_db()
            cur = conn.cursor()
            cur.execute('insert into students(first_name,middle_name,last_name,dob,state_of_origin,email,jamb_score,gender,phone,address,local_gov,next_of_kin) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',(s_fname,s_mname,s_lname,s_dob,s_state,s_email,s_score,s_gndr,s_phone,s_addr,s_lg,s_kin))
            conn.commit()
            conn.close()
            flash('Student added successfully','success')
            return redirect(url_for('home'))

@app.route("/student_details",methods=["GET","POST"])
def student_details():
    return render_template("student_details.html")

@app.route("/students_index",methods=["GET","POST"])
def students_index():
    return render_template("students_index.html")
if __name__ == "__main__":
    app.run(debug=True)