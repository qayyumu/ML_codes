from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__,template_folder='template')  ##folder name

#ububtu use:      export SQL_URI="postgresql://username:password@server:5433/db_name"
#windows:         set SQL_URI=postgresql://username:password@<server:5433/db_name
#Example "        set SQL_URI=postgresql://postgres:Providepassword@localhost:5433/empl  
###set SECRET_key_for_session=secretkey

# print(os.getenv("SQL_URI"))
# print(os.getenv("SECRET_key_for_session"))

if(1):   ## load the env variables from the .env filepath
   from dotenv import load_dotenv
   load_dotenv('.env')

print("Path to the SQL:", os.getenv("SQL_URI"))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQL_URI")
app.secret_key = os.getenv("SECRET_key_for_session")
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
         flash('Please enter all the fields', 'error')
      else:
         employee = employees(request.form['name'], request.form['city'],request.form['addr'], request.form['pin'])
         db.session.add(employee)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

if __name__ == '__main__':
   with app.app_context():
        db.create_all()
   app.run(debug = True)