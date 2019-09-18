#import dependencies
from flask import Flask, render_template
from flask import request, redirect
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields import (StringField, DateField, IntegerField, SubmitField)
from wtforms.validators import DataRequired
from wtforms.validators import Email, EqualTo, InputRequired, Length

#initialize app
#app = Flask(__name__)

#
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:root@localhost/patients'
db = SQLAlchemy(app)

#if __name__ == '__main__':
    #app.run(debug=True)


class Patient(db.Model):
    __tablename__ = 'document'
    mR = db.Column('medicalRecordNum', db.String, primary_key=True)
    rN = db.Column('requesterName', db.String(50))
    pN = db.Column('patientName', db.String(50))
    rN = db.Column('date', db.Date)
    rN = db.Column('comment', db.Text)

#create patient entry form
class PatientEntry(FlaskForm):
    requesterName = StringField(
        'Requester name', validators=[InputRequired(),Length(1, 50)])
    patientName = StringField(
        'Patient name', validators=[InputRequired(),Length(1, 50)])
    medicalRecordNum = StringField(
        'Medical Record Number')
    dateReceived = DateField('Date Received', format= '%Y-%m-%d')
    comments = StringField(
        'Comments', validators=[InputRequired(),Length(1, 60)])
    #submit=SubmitField('Enter Patient')

@app.route('/', methods=['POST'])
def form():
    form = PatientEntry()
    if form.validate_on_submit():
        patient = Patient(request.form('medicalRecordNum'),request.Form('requesterName'),request.form('patientName'),request.Form('dateReceived'),
        request.form('comments'))
        db.session.add(patient)
        db.session.commit()
        return render_template('patients.html',form=form)
    return render_template('form.html',form=form)

@app.route('/patients', methods=['GET'])
def patients():
    form = PatientEntry()
    if form.validate_on_submit():
        return render_template('patient_submitted.html',form=form)
    return render_template('patients.html',form=form)
