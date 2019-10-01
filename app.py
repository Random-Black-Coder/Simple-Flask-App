#import dependencies
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator

#initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ulghmdxtcavxmn:89d1c941ddeaa99801a8b3e2bafe7f86e6a2d9e6ff29f00d38fb987751b01462@ec2-54-221-215-228.compute-1.amazonaws.com:5432/dc4bvr7gb74u5n'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:root@localhost/Patients'
db = SQLAlchemy(app)
nav = Nav(app)
Bootstrap(app)

#build navbar
nav.register_element('my_navbar', Navbar('thenav', View('Home Page','show_all')))

#patient Database object
class Patients(db.Model):
    __tablename__ = 'patients'
    requesterName = db.Column(db.String(50))
    patientName = db.Column(db.String(50))
    medicalRecordNumber = db.Column(db.String, primary_key=True)
    dateReceived = db.Column(db.Date)
    comments = db.Column(db.String(60))

    #patient constructor
    def __init__(self, requesterName, patientName, medicalRecordNumber, dateReceived, comments):
        self.requesterName = requesterName
        self.patientName = patientName
        self.medicalRecordNumber = medicalRecordNumber
        self.dateReceived = dateReceived
        self.comments = comments

#homepage
@app.route('/')
def show_all():
    return render_template('show_all.html', patients = Patients.query.all())

#patient entry form
@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['requesterName'] or not request.form['patientName'] or not request.form['medicalRecordNumber'] or not request.form['dateReceived']:
         flash('Please enter all the fields', 'error')
      else:
         patient = Patients(request.form['requesterName'], request.form['patientName'],
            request.form['medicalRecordNumber'], request.form['dateReceived'], request.form['comments'])

         db.session.add(patient)
         db.session.commit()

         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

#patient deletion form
@app.route('/delete', methods = ['GET', 'POST'])
def delete():
   if request.method == 'POST':
      if not request.form['medicalRecordNumber']:
         flash('Please enter the patients medical record number.', 'error')
      else:
          mrn = request.form['medicalRecordNumber']
          patient = Patients.query.filter_by(medicalRecordNumber=mrn).first()

          db.session.delete(patient)
          db.session.commit()

          flash('Record was successfully removed')
          return redirect(url_for('show_all'))
   return render_template('delete.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
