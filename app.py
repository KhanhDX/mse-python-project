from flask import Flask, render_template, request, redirect, url_for, flash
from data_access import StudentDataAccess

app = Flask(__name__)
app.secret_key = "Secret Key"

studentData = StudentDataAccess()
conn = studentData.createConnection("PPR501Assignment.db")

@app.route('/')
def index():
    allData = studentData.getAll(conn)
    return render_template('index.html', students = allData)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        rnumber = request.form['rnumber']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        dob = request.form['dob']
        address = request.form['address']
        score = request.form['score']
        info =(rnumber, fname, lname, email, dob, address, score)
        studentData.createStudent(conn, info)
        flash("Student inserted successfully!")
    return redirect(url_for('index'))

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        rnumber = request.form['hid_rnumber']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        dob = request.form['dob']
        address = request.form['address']
        score = request.form['score']
        info =(fname, lname, email, dob, address, score, rnumber)
        studentData.updateStudent(conn, info)
        flash("Student updated successfully!")
    return redirect(url_for('index'))

@app.route('/delete/<rnumber>/', methods = ['GET', 'POST'])
def delete(rnumber):
    studentData.deleteStudent(conn, rnumber)
    flash("Student deleted successfully!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
