import sqlite3

CONN = sqlite3.connect("school.db")
CURSOR = CONN.cursor()

def create_table():
    CURSOR.execute("""CREATE TABLE IF NOT EXISTS tms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name VARCHAR(20) NOT NULL,
                    last_name VARCHAR(20) NOT NULL
    )""")

    CURSOR.execute("""CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                first_name VARCHAR(20) NOT NULL,
                last_name VARCHAR(25) NOT NULL,
                tm_id INTEGER,
                FOREIGN KEY (tm_id) REFERENCES tms(id)
    )""")

    CONN.commit()
    CONN.close()
create_table()



class SchoolDb():
    def __init__(self):
        self.CONN = sqlite3.connect("school.db")
        self.CURSOR = self.CONN.cursor()


    def add_tm(self, first_name, last_name):
        self.CURSOR.execute("INSERT INTO tms (first_name, last_name) VALUES (?, ?)",
                            (first_name, last_name))
        self.CONN.commit()


    def add_student(self, first_name, last_name):
        self.CURSOR.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)",
                            (first_name, last_name))
        self.CONN.commit()


    def tm_exists(self, tm_id):
        self.CURSOR.execute("SELECT * FROM tms WHERE id = ?", (tm_id,))
        return self.CURSOR.fetchone() is not None
    

    def assign_tm_to_student(self, student_id, tm_id):
        if self.tm_exists(tm_id):
            self.CURSOR.execute("UPDATE students SET tm_id = ? WHERE id = ?",
                                (tm_id, student_id))
            self.CONN.commit()
            print(f"TM {tm_id} assigned to student {student_id}")
        else:
            print(f"Tm with ID {tm_id} does not exist.")


    def list_tms(self):
        self.CURSOR.execute("SELECT * FROM tms")
        return self.CURSOR.fetchall()
    
    
    def list_students(self):
        query = """
            SELECT students.id, students.first_name, students.last_name,
            tms.id, tms.first_name, tms.last_name
            FROM students
            LEFT JOIN tms ON students.tm_id = tms.id
        """
        self.CURSOR.execute(query)
        return self.CURSOR.fetchall()
    

    def close(self):
        self.CONN.close()


def main():
    db = SchoolDb()
    while True:
        print("\n1. Add TM")
        print("2. Add Student")
        print("3. Assign TM to Student")
        print("4. List TMs")
        print("5. List Students")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            first_name = input("Enter TM's first name: ")
            last_name = input("Enter TM's last name: ")
            db.add_tm(first_name, last_name)

        elif choice == "2":
            first_name = input("Enter Students's first name: ")
            last_name = input("Enter Students's last name: ")
            db.add_student(first_name,last_name)

        elif choice == "3":
            student_id = int(input("Enter Student's ID: "))
            tm_id = int(input("Enter TM's ID: "))
            db.assign_tm_to_student(student_id, tm_id)

        elif choice == "4":
            tms = db.list_tms()
            for tm in tms:
                print(f" TM ID: {tm[0]}, First Name: {tm[1]}, Last Name: {tm[2]}")

        elif choice == '5':
            students = db.list_students()
            for student in students:
                if student[3] is not None:
                    print(f"Student ID: {student[0]}, First Name: {student[1]}, Last Name: {student[2]}, TM ID: {student[3]}, TM First Name: {student[4]},TM Last Name: {student[5]} ")
                else:
                    print(f"Student ID: {student[0]}, Student First Name: {student[1]}, Student Last Name: {student[2]}, TM: None")
        elif choice == '6':
            db.close()
            break
        else:
            print("Invalid choice. Please try again")  

if __name__ == '__main__':
    main()  
            

    