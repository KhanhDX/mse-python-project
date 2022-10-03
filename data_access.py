import sqlite3
from student import Student

class StudentDataAccess:
    def createConnection(self, dbName):
        conn = None
        try:
            conn = sqlite3.connect(dbName, check_same_thread=False)
            if conn is not None:
                cur = conn.cursor()
                self.createTable(conn)
            else:
                raise Exception("Cannot create the database connection.")
        except Exception as e:
            print(e)
        return conn

    def createTable(self, conn):
        sql_create_table = """CREATE TABLE IF NOT EXISTS student (
                                            roll_number text PRIMARY KEY,
                                            first_name text NOT NULL,
                                            last_name text NOT NULL,
                                            email text NOT NULL,
                                            date_of_birth text NOT NULL,
                                            address text NOT NULL,
                                            score real NOT NULL
                                        )"""
        conn.cursor().execute(sql_create_table)

    def getAll(self, conn):
        sql_select = """SELECT roll_number, first_name, last_name, email, date_of_birth, address, score FROM student"""
        lst = conn.cursor().execute(sql_select).fetchall()
        students = []
        for item in lst:
            s = Student(item)
            students.append(s)
        return students


    def createStudent(self, conn, info):
        sql_insert = """INSERT INTO student VALUES(?, ?, ?, ?, ?, ?, ?)"""
        conn.cursor().execute(sql_insert, info)
        conn.commit()

    def updateStudent(self, conn, info):
        sql_update = """UPDATE student
                        SET first_name = ? ,
                            last_name = ? ,
                            email = ? ,
                            date_of_birth = ? ,
                            address = ? ,
                            score = ?
                        WHERE roll_number = ?"""
        conn.cursor().execute(sql_update, info)
        conn.commit()

    def deleteStudent(self, conn, rnumber):
        sql_delete = """DELETE FROM student WHERE roll_number=?"""
        conn.cursor().execute(sql_delete, (rnumber,))
        conn.commit()