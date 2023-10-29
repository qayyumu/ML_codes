
from flask_cors import CORS
import logging
import os
logFile = 'sample.log'
# logFile = "C:\\WebApplication1\\flaskapp\\samplelog.log"

import re

from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__,template_folder='template')  ##folder name
CORS(app, resources={r"/api/*": {"origins": "*"}})

#ububtu use:      export SQL_URI="postgresql://username:password@server:5433/db_name"
#windows:         set SQL_URI=postgresql://username:password@<server:5433/db_name
#Example "        set SQL_URI=postgresql://postgres:Providepassword@localhost:5433/empl  
###set SECRET_key_for_session=secretkey

# print(os.getenv("SQL_URI"))
# print(os.getenv("SECRET_key_for_session"))

# if(1):   
#    from dotenv import load_dotenv
#    load_dotenv('.env')
from myenv import SQL_URI, SECRET_key_for_session ## load the env variables from the .env filepath



# print("Path to the SQL:", os.getenv("SQL_URI"))
app.config["SQLALCHEMY_DATABASE_URI"] = SQL_URI #os.getenv("SQL_URI")
app.secret_key = SECRET_key_for_session #os.getenv("SECRET_key_for_session")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class employees(db.Model):
   id = db.Column('employee_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))
   addr = db.Column(db.String(200)) 
   pin = db.Column(db.String(10))

   def __init__(self, name, city, addr,pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

@app.route('/')
def show_all():
   return render_template('show_all.html', employees = employees.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         print('Data form not filled')
         flash('Please enter all the fields', 'error')
      else:
         employee = employees(request.form['name'], request.form['city'],request.form['addr'], request.form['pin'])
         db.session.add(employee)
         db.session.commit()
         print('Record added')
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

@app.route('/deletee', methods = ['GET', 'POST'])
def deletee():
   if request.method == 'POST':
      if not request.form['name']:
         print('Data form not filled')
         flash('Please enter all the fields', 'error')
      else:
         #### check if the employee exist in the database  --retreive from the database
         obtain_emp = db.session.query(employees).filter_by(name=request.form['name']).first()
         if(obtain_emp):
            print(obtain_emp.name,obtain_emp.id)
            # employee = employees(request.form['name'], "","","")
            db.session.delete(obtain_emp)
            db.session.commit()
            print('Record deleted')
            flash('Record was successfully deleted')
            return redirect(url_for('show_all'))
         else:
            print('Record not found')
            flash('Record was not found')
            return redirect(url_for('show_all'))
   return render_template('delete.html')



if __name__ == '__main__':
   with app.app_context():
        db.create_all()
   app.run(debug = True)