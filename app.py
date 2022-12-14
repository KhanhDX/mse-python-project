import re
import sqlite3

import urllib

from flask import Flask, render_template, request, redirect, url_for, flash

from data_access import StudentDataAccess
from student import Student


import json

app = Flask(__name__)
app.secret_key = "Secret Key"

studentData = StudentDataAccess("PPR501Assignment.db")

@app.route('/')
def index():
    allData = studentData.getAll()
    return render_template('index.html', students = allData)

@app.route('/exportData')
def exportAll():
    allData = studentData.getAll()
    res = json.dumps([s.dump() for s in allData], ensure_ascii=False)
    return res

@app.route('/exportData/<rnumber>/')
def exportOne(rnumber):
    student = studentData.get(rnumber)
    res = json.dumps(student.dump(), ensure_ascii=False) if student is not None else {}
    return res

def extractForm(request):
    rnumber = request.form['rnumber']
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    dob = request.form['dob']
    address = request.form['address']
    score = request.form['score']

    checkIsBlank([rnumber, fname, lname, email, dob, address, score])
    checkValidateEmail(email)

    return rnumber, fname, lname, email, dob, address, score

def checkValidateEmail(email):
    regexEmail = r'^\S+@\S+\.\S+$'
    if not (re.fullmatch(regexEmail, email)):
        flash('Invalid Email')
        raise Exception('Invalid Email')
def checkIsBlank(input):
    for text in input:
        if(text.strip()==''):
            flash('Input cannot be null or empty');
            raise Exception ('Input cannot be null or empty')

@app.route('/insert', methods = ['POST'])
def insert():
    try:
        stdData = Student(extractForm(request))
        studentData.createStudent(stdData)
        flash("Student inserted successfully!")
    except Exception as e:
        print(e)
        if type(e) is sqlite3.IntegrityError: flash("Roll number is existed!")
        flash("Student insert failed!")
    return redirect(url_for('index'))

@app.route('/update', methods = ['POST'])
def update():
    try:
        stdData = Student(extractForm(request))
        studentData.updateStudent(stdData)
        flash("Student updated successfully!")
    except Exception as e:
        print(e)
        flash("Student update failed!")
    return redirect(url_for('index'))

@app.route('/delete/<rnumber>/', methods = ['GET'])
def delete(rnumber):
    try:
        studentData.deleteStudent(rnumber)
        flash("Student deleted successfully!")
    except Exception as e:
        print(e)
        flash("Student delete failed!")
    return redirect(url_for('index'))

# @app.route('/exportData-to-txt', methods = ['GET'])
# def exportDataToFile():
#     allData = studentData.getAll()
#     with open('datafile.txt', 'w', encoding='utf-8') as xfile:
#         for item in allData:
#             xfile.write("%s \t %s %s \t %s \t %s \t %s \t %d\n" %item.data())
#     flash("Export file successfully!")
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
