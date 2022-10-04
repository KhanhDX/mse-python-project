import sqlite3
from student import Student

class StudentDataAccess:
    def __init__(self, dbName):
        self.conn = None
        try:
            self.conn = sqlite3.connect(dbName, check_same_thread=False)
            if self.conn is not None:
                self.createTable()
            else:
                raise Exception("Cannot create the database connection.")
        except Exception as e:
            print(e)

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def createTable(self):
        sql_create_table = """CREATE TABLE IF NOT EXISTS student (
                                            roll_number text PRIMARY KEY,
                                            first_name text NOT NULL,
                                            last_name text NOT NULL,
                                            email text NOT NULL,
                                            date_of_birth text NOT NULL,
                                            address text NOT NULL,
                                            score real NOT NULL
                                        )"""
        self.conn.cursor().execute(sql_create_table)

    def getAll(self):
        sql_select = """SELECT roll_number, first_name, last_name, email, date_of_birth, address, score FROM student"""
        lst = self.conn.cursor().execute(sql_select).fetchall()
        students = []
        for item in lst:
            s = Student(item)
            students.append(s)
        return students

    def get(self, rnumber):
        sql_select = """SELECT roll_number, first_name, last_name, email, date_of_birth, address, score FROM student WHERE roll_number = :rnumber"""
        student = self.conn.cursor().execute(sql_select, {'rnumber': rnumber}).fetchone()
        return Student(student) if student is not None else None

    def createStudent(self, std):
        sql_insert = """INSERT INTO student VALUES(?, ?, ?, ?, ?, ?, ?)"""
        self.conn.cursor().execute(sql_insert, std.data())
        self.conn.commit()

    def updateStudent(self, std):
        sql_update = """UPDATE student
                        SET first_name = ? ,
                            last_name = ? ,
                            email = ? ,
                            date_of_birth = ? ,
                            address = ? ,
                            score = ?
                        WHERE roll_number = ?"""
        self.conn.cursor().execute(sql_update, std.data(True))
        self.conn.commit()

    def deleteStudent(self, rnumber):
        sql_delete = """DELETE FROM student WHERE roll_number=?"""
        self.conn.cursor().execute(sql_delete, (rnumber,))
        self.conn.commit()