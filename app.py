from __future__ import print_function
from flask import Flask, render_template, url_for, request,flash,redirect,session
from flask_restplus import Api
#from flask.ext.restplus import Api
from dbconnect import connection
from wtforms import Form, TextField, PasswordField,validators,RadioField
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
import gc


import sys



app = Flask(__name__)

app.secret_key = 'my unobvious secret key'



@app.route('/')
def home():
    return render_template('index.html')




@app.route('/data', methods=["GET","POST"])
def data():
	return render_template('data.html')

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            error = "You need to login first"
            return redirect(url_for('login', error = error))

    return wrap


@app.route("/logout")
@login_required
def logout():
    session.clear()
    error = "You have been logged out!"
    gc.collect()
    return redirect(url_for('login',error = error))



@app.route('/login', methods=["GET","POST"])
def login():

    error = ''
    try:
    	c, conn = connection()
    	if (request.method == "GET"):
            return render_template("login.html")
        
    	if (request.method == "POST"):
            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                             (thwart(request.form['username']),))
            data = c.fetchone()[1]

            #return data

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for("data"))
				
            else:
            	error = "Invalid credentials. Try Again."

            gc.collect()

            return render_template("login.html", error = error)
        

    except Exception as e:
        return(str(e))
        error = "Invalid credentials. Try Again. 2"
        return render_template("login.html", error = error)




@app.route('/signup', methods=["GET","POST"])
def signup():
    try:
        form = RegistrationForm(request.form)

        
        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()
            #return render_template("signup.html", form=c)

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username),))

            if int(x) > 0:
                err = "That username is already taken, please choose another"
                return render_template('signup.html', form=form,error = err)

            else:
                c.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email)))
                
                conn.commit()
                res = "Thanks for registering!"
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username
                a = session['username']

                return redirect(url_for('data',name = username))

        return render_template("signup.html", form=form)

    except Exception as e:
        return(str(e))







class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class radiofrm(Form):
    one = RadioField()



   
    







@app.route('/result', methods=['POST', 'GET'])
def result():
	error = ''
	try:
		if request.method == 'POST':

			branch = request.form['branch']
			ssc = request.form['ssc']
			hsc = request.form['hsc']
			sem1 = request.form['sem1']
			sem2 = request.form['sem2']
			sem3 = request.form['sem3']
			sem4 = request.form['sem4']
			sem5 = request.form['sem5']
			sem6 = request.form['sem6']
			kt = request.form['kt']
			dkt = request.form['dkt']
			total = request.form['total']


			extraversion = request.form['extraversion']
			agreeableness = request.form['agreeableness']
			openness = request.form['openness']
			conscientiousness = request.form['conscientiousness']
			neuroticism = request.form['neuroticism']

			one = request.form['one']




			from pandas import DataFrame
			df = DataFrame([[
				agreeableness,
				conscientiousness,
				extraversion,
				neuroticism,
				openness,
				branch,
				dkt,
				hsc,
				kt,
				sem1,
				sem2,
				sem3,
				sem4,
				sem5,
				sem6,
				ssc,
				total
				

				]])

			from sklearn.externals import joblib
			aclf = joblib.load('nba.pkl');

			result = aclf.predict(df)
			if(result[0] == 1.0): 
				result = "employed" 
			else:
				result ="not employed"


			from sklearn.externals import joblib
			cd = joblib.load('reccc.pkl')

			b = cd.predict(total, hsc)
			bd=b.est
			
			

			if(bd <= 1.0): 
				a = "Software Engineer - IT services"
			elif(bd <= 2.0):
				a = "Software Engineer - IT Product"
			elif(bd <= 3.0):
				a = "Associate - ITES Operation"
			elif(bd <= 4.0):
				a = "Business Analyst"
			elif(bd <= 5.0):
				a = "creative content developer"
			else:
				a = "error"















			


			


	         
		      

			
		return render_template("result.html", result = result,score=a)

	except Exception as e:
		flash(e)
		return render_template("data.html", error = error)


  



if __name__ == '__main__':
    app.run(debug=True)
