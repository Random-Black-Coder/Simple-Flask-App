#import dependencies
from flask import Flask, render_template
from flask import request, redirect
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy


#initialize app
app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)

#
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yahkeef:root@localhost/patients'
db = SQLAlchemy(app)

#patient oject
class Patient(db.Model):
    __tablename__ = 'documents'
    mR = db.Column(db.String, primary_key=True)
    rN = db.Column(db.String(50))
    pN = db.Column(db.String(50))
    rN = db.Column(db.Date)
    rN = db.Column(db.String(60))

#homepage
@app.route('/')
def index():
    return render_template('form.html')

#patient entry form
@app.route('/post_patient', methods=['POST'])
def post_patient():
    patient = Patient(request.form('medicalRecordNum'),request.form('requesterName'),request.form('patientName'),request.form('dateReceived'),
    request.form('comments'))
    db.session.add(patient)
    db.session.commit()
    return render_template(url_for('index'))
