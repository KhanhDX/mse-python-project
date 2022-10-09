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

@app.route('/insert', methods = ['POST'])
def insert():
    try:
        rnumber = request.form['rnumber']
        checkDuplicate = studentData.get(rnumber.strip())
        if checkDuplicate is not None:
            flash('Roll number is existed!')
            raise Exception()
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        dob = request.form['dob']
        address = request.form['address']
        score = request.form['score']
        stdData = Student([rnumber, fname, lname, email, dob, address, score])
        studentData.createStudent(stdData)
        flash("Student inserted successfully!")
    except Exception as e:
        print(e)
        flash("Student insert failed!")
    return redirect(url_for('index'))

@app.route('/update', methods = ['POST'])
def update():
    try:
        rnumber = request.form['hid_rnumber']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        dob = request.form['dob']
        address = request.form['address']
        score = request.form['score']
        stdData = Student([rnumber, fname, lname, email, dob, address, score])
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

@app.route('/exportData-to-txt', methods = ['GET'])
def exportDataToFile():
    allData = studentData.getAll()
    with open('datafile.txt', 'w', encoding='utf-8') as xfile:
        for item in allData:
            xfile.write("%s \t %s %s \t %s \t %s \t %s \t %d\n" %item.data())
    flash("Export file successfully!")
    return redirect(url_for('index'))

def crawlData():

    lst = []
    url = "http://127.0.0.1:5000/"
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('td')
    for i in range(0, len(tags), 8):
        data = ''
        data = data + 'RollNumber:' + tags[i].text + '\n'
        data = data + 'First Name:' + tags[i].text + '\n'
        data = data + 'Last Name:' + tags[i].text + '\n'
        data = data + 'Email:' + tags[i].text + '\n'
        data = data + 'Date of birth:' + tags[i].text + '\n'
        data = data + 'Address:' + tags[i].text + '\n'
        data = data + 'Score:' + tags[i].text + '\n'
        lst.append(data)
    with open('dataCrawl.txt', 'w') as file:
        for i in range(0, len(lst)):
            s = 'Thong tin sinh vien thu: '
            s = s + str(i + 1) + '\n'
            file.write(s)
            file.write(lst[i])
            file.write("\n")

if __name__ == '__main__':
    app.run(debug=True)
    crawlData()
