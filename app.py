#import dependencies
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy

#initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:root@localhost/Patients'
db = SQLAlchemy(app)

#patient oject
class Patients(db.Model):
    __tablename__ = 'patients'
    requesterName = db.Column(db.String(50))
    patientName = db.Column(db.String(50))
    medicalRecordNumber = db.Column(db.String, primary_key=True)
    dateReceived = db.Column(db.Date)
    comments = db.Column(db.String(60))

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


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
