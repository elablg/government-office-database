import sqlite3


conn = sqlite3.connect("government_office.db")
cursor = conn.cursor()


# creating the tables according to my ER diagram


# Enabling the  foreign key constraints in SQLite
conn.execute('PRAGMA foreign_keys = ON;')


# DEPARTMENT table
cursor.execute('''
CREATE TABLE IF NOT EXISTS DEPARTMENT(
    department_ID INTEGER PRIMARY KEY,
    department_name TEXT
)
''')

# EMPLOYEE table
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS EMPLOYEE(
    employee_ID INTEGER PRIMARY KEY,
    fname TEXT, 
    lname TEXT,
    email TEXT,
    salary REAL,
    department_ID INTEGER, -- links to DEPARTMENT -> without a department_ID column you cannot create a foreign key since a foreign key must refer to a column.
    FOREIGN KEY(department_ID) REFERENCES DEPARTMENT(department_ID) -- this ensures that you cannot assign an employee that does not exist in a department
    )
''')

# SERVICE table
cursor.execute('''
CREATE TABLE IF NOT EXISTS SERVICE(
    service_ID INTEGER PRIMARY KEY,
    service_name TEXT,
    availability TEXT,
    department_ID INTEGER, -- links to DEPARTMENT 
    FOREIGN KEY (department_ID) REFERENCES DEPARTMENT(department_ID) -- each service is offered by a department therefore this ensures that you cannot define a service if its not connected to a valid department

)
''')

#PROJECT table
cursor.execute('''
CREATE TABLE IF NOT EXISTS PROJECT(
    project_ID INTEGER PRIMARY KEY,
    project_name TEXT,
    status TEXT,
    budget REAL,
    department_ID INTEGER, -- links to DEPARTMENT
    FOREIGN KEY (department_ID) REFERENCES DEPARTMENT(department_ID) -- this ensures all projects are associated with an existing department

)
''')

# CITIZEN table
cursor.execute('''
CREATE TABLE IF NOT EXISTS CITIZEN(
citizen_ID INTEGER PRIMARY KEY,
address TEXT
)
''')

# CITIZEN_TEL table since 'tel' is a multivalued attribute
cursor.execute('''
CREATE TABLE IF NOT EXISTS CITIZEN_TEL(
citizen_ID INTEGER,
tel TEXT, 
PRIMARY KEY (citizen_ID, tel), -- both are primary key here just like in relational schema
FOREIGN KEY (citizen_ID) REFERENCES CITIZEN(citizen_ID)
)
''')


# WORKS_ON table
cursor.execute('''
CREATE TABLE IF NOT EXISTS WORKS_ON(
    employee_ID INTEGER,
    project_ID INTEGER,
    start_date TEXT,
    end_date TEXT,
    PRIMARY KEY(employee_ID, project_ID),
    FOREIGN KEY(employee_ID) REFERENCES EMPLOYEE(employee_ID), -- these are foreign keys because they establish a relationship between the WORKS_ON table EMPLOYEE ajnd PROJECT table
    FOREIGN KEY(project_ID) REFERENCES PROJECT(project_ID)
)
''')

# REQUESTS table
cursor.execute('''
CREATE TABLE IF NOT EXISTS REQUESTS(
    service_ID INTEGER,
    citizen_ID INTEGER,
    request_date TEXT,
    PRIMARY KEY(service_ID, citizen_ID),
    FOREIGN KEY(service_ID) REFERENCES SERVICE(service_ID), 
    FOREIGN KEY(citizen_ID) REFERENCES CITIZEN(citizen_ID)
)
''')

# WORKS_FOR table
cursor.execute('''
CREATE TABLE IF NOT EXISTS WORKS_FOR(
    employee_ID INTEGER,
    department_ID INTEGER,
    PRIMARY KEY(employee_ID, department_ID),
    FOREIGN KEY(employee_ID) REFERENCES EMPLOYEE(employee_ID),
    FOREIGN KEY(department_ID) REFERENCES DEPARTMENT(department_ID)
)
''')

# OFFERS table
cursor.execute('''
CREATE TABLE IF NOT EXISTS OFFERS(
    department_ID INTEGER,
    service_ID INTEGER,
    PRIMARY KEY(department_ID, service_ID),
    FOREIGN KEY(department_ID) REFERENCES DEPARTMENT(department_ID),
    FOREIGN KEY(service_ID) REFERENCES SERVICE(service_ID)
)
''')

# CONTROLS table
cursor.execute('''
CREATE TABLE IF NOT EXISTS CONTROLS(
    department_ID INTEGER,
    project_ID INTEGER,
    PRIMARY KEY(department_ID, project_ID),
    FOREIGN KEY(department_ID) REFERENCES DEPARTMENT(department_ID),
    FOREIGN KEY(project_ID) REFERENCES PROJECT(project_ID)
)
''')


# inserting values into the tables

#inserting values into DEPARTMENT table
department_rows = [
    (1001, "Administration"),
    (1002, "Finance"),
    (1003, "Education"),
    (1004, "Public Relations"),
    (1005, "Information Technology")
]

cursor.executemany("INSERT OR IGNORE INTO DEPARTMENT(department_ID, department_name) VALUES (?, ?)", department_rows)

#inserting values into EMPLOYEE table
employee_rows = [
    (1, "Ela", "Bilgisu", "elabilgisu@gmail.com", 50000.00, 1002),
    (2, "Selin", "Aydın", "selinaydin@gmail.com", 45000.00, 1001),
    (3, "Zeynep", "Günçe", "zeynepgunce@gmail.com", 40000.00, 1004),
    (4, "Ali", "Kaplan", "alikaplan@gmail.com", 55000.00, 1005),
    (5, "Ulaş", "Akcan", "ulasakcan@gmail.com", 35000.00, 1003),
    (6, "Dila", "Orhan", "dilaorhan@gmail.com", 45000.00, 1004)
]
cursor.executemany("INSERT OR IGNORE INTO EMPLOYEE(employee_ID, fname, lname, email, salary, department_ID) VALUES (?, ?, ?, ?, ?, ?)", employee_rows)

#inserting values into PROJECT table
project_rows = [
    (11, "Paperless Office Transformation", "Ongoing", 750000.00, 1005),
    (12, "2025-2026 High School Curriculum Report", "Finished", 500000.00, 1003),
    (13, "2025 Retirement Salary Planning", "Finished", 25000.00, 1002),
    (14, "Employee Satisfaction Survey", "Ongoing", 5000.00, 1001),
    (15, "Diversity and Inclusion Strategy", "Not Started", 50000.00, 1004)
]
cursor.executemany("INSERT OR IGNORE INTO PROJECT(project_ID, project_name, status, budget, department_ID) VALUES(?, ?, ?, ?, ?)", project_rows)

# inserting values into SERVICE table
service_rows = [
     (101, "Tax Consultation for Elderly", "Available", 1002),
     (102, "Elementary School Teacher Training", "Not available", 1003),
     (103, "IT Support", "Available", 1005),
     (104, "Registered Record Center", "Not Available", 1001),
     (105, "Social Media Account Management", "Available", 1004)
]
cursor.executemany("INSERT OR IGNORE INTO SERVICE(service_ID, service_name, availability, department_ID) VALUES(?, ?, ?, ?)", service_rows)

# inserting values into CITIZEN table
citizen_rows = [
    (10001, "Kocaeli, Türkiye"),
    (10002, "Istanbul, Türkiye"),
    (10003, "Ankara, Türkiye"),
    (10004, "Bilecik, Türkiye"),
    (10005, "Eskişehir, Türkiye")
]
cursor.executemany("INSERT OR IGNORE INTO CITIZEN(citizen_ID, address) VALUES(?, ?)",citizen_rows)

# inserting values into CITIZEN_TEL table
citizen_tel_rows = [
    (10001, "111-111"),
    (10002, "222-222"),
    (10003, "333-333"),
    (10004, "444-444"),
    (10005, "555-555")
]
cursor.executemany("INSERT OR IGNORE INTO CITIZEN_TEL(citizen_ID, tel) VALUES(?, ?)", citizen_tel_rows)

# inserting values into relationships

# inserting values into WORKS_ON table
works_on_rows = [
    (1, 11, "2023-01-01", "2023-05-06"),
    (2, 11, "2023-01-01", "2023-16-15"),
    (3, 13, "2023-04-16", "2024-01-20"),
    (4, 15, "2023-09-21", "2024-02-12"),
    (5, 14, "2023-11-11", "2024-05-06"),
    (5, 12, "2023-12-12", "2024-10-18")
]
cursor.executemany("INSERT OR IGNORE INTO WORKS_ON(employee_ID, project_ID, start_date, end_date) VALUES(?, ?, ?, ?)", works_on_rows)

# inserting values into REQUESTS table
requests_rows = [
    (101, 10002, "2024-12-20"),
    (101, 10003, "2024-09-09"),
    (103, 10005, "2023-10-25"),
    (102,10004, "2024-06-13"),
    (104, 10002, "2024-09-12")
]
cursor.executemany("INSERT OR IGNORE INTO REQUESTS(service_ID, citizen_ID, request_date) VALUES(?, ?, ?)", requests_rows)

# inserting values into WORKS_FOR table
works_for_rows = [
    (1, 1001),
    (2, 1001),
    (3, 1002),
    (4, 1003),
    (5, 1004),
    (6, 1002)
]
cursor.executemany("INSERT OR IGNORE INTO WORKS_FOR(employee_ID, department_ID) VALUES(?, ?)", works_for_rows)

# inserting values into OFFERS table
offers_rows = [
    (1001, 101),
    (1002, 102),
    (1003, 103),
    (1003, 101),
    (1004, 104),
    (1005, 105)
]
cursor.executemany("INSERT OR IGNORE INTO OFFERS(department_ID, service_ID) VALUES(?, ?)", offers_rows)

# inserting values into CONTROLS table
controls_rows = [
    (1001, 11),
    (1002, 12),
    (1003, 13),
    (1004, 14),
    (1004, 15),
    (1005, 15)
]
cursor.executemany("INSERT OR IGNORE INTO CONTROLS(department_ID, project_ID) VALUES(?, ?)", controls_rows)

conn.commit()


try:
    conn.execute('PRAGMA foreign_keys = ON;')
    print("Foreign key enforcement enabled.")
except sqlite3.Error as e:
    print("Error enabling foreign keys:", e)

print("Tables created successfully.")


# Insert data into tables
try:
    # (Add all your INSERT statements here)
    conn.commit()
    print("Data inserted successfully.")
except sqlite3.Error as e:
    print("Error inserting data:", e)

print("Data inserted into DEPARTMENT table.")

"""
deneme
cursor.execute("SELECT * FROM DEPARTMENT")
print(cursor.fetchall())
"""

# user adding records to any table they want
def add_records():
    try:
        # using the input function to get the data from the user
        table_to_add = input("Enter table name to add a record (or type 'QUIT' to quit): ").strip()  # strip() removes extra spaces
        if table_to_add.upper() == "QUIT":
            print("Add records function is stopped.")
            return  # ends the function

        if table_to_add.upper() == "EMPLOYEE":
            employee_ID = int(input("Enter employee ID: "))
            fname = input("Enter first name: ")
            lname = input("Enter last name: ")
            email = input("Enter email: ")
            salary = float(input("Enter salary: "))
            department_ID = int(input("Enter department_ID: "))

            # Executing SQL query
            cursor.execute(
                "INSERT OR IGNORE INTO EMPLOYEE(employee_ID, fname, lname, email, salary, department_ID) VALUES (?, ?, ?, ?, ?, ?)",
                (employee_ID, fname, lname, email, salary, department_ID)
            )

        elif table_to_add.upper() == "DEPARTMENT":
            department_ID = int(input("Enter department ID: "))
            department_name = input("Enter department name: ")

            cursor.execute(
                "INSERT OR IGNORE INTO DEPARTMENT(department_ID, department_name) VALUES (?, ?)",
                (department_ID, department_name)
            )

        elif table_to_add.upper() == "PROJECT":
            project_ID = int(input("Enter project ID: "))
            project_name = input("Enter project name: ")
            status = input("Enter current status: ")
            budget = float(input("Enter the budget: "))
            department_ID = int(input("Enter the department ID: "))

            cursor.execute(
                "INSERT OR IGNORE INTO PROJECT(project_ID, project_name, status, budget, department_ID) VALUES (?, ?, ?, ?, ?)",
                (project_ID, project_name, status, budget, department_ID)
            )
        elif table_to_add.upper() == "SERVICE":
            service_ID = int(input("Enter service ID: "))
            service_name = input("Enter service name: ")
            availability = input("Enter availability: ")
            department_ID = int(input("Enter department ID: "))

            cursor.execute("INSERT OR INGORE INTO SERVICE(service_ID, service_name, availability, department_ID) VALUES(?, ?, ?, ?)",
            (service_ID, service_name, availability, department_ID)
            )


        elif table_to_add.upper() == "CITIZEN":
            citizen_ID = int(input("Enter citizen ID: "))
            address = input("Enter the address of the citizen: ")

            cursor.execute(
                "INSERT OR IGNORE INTO CITIZEN(citizen_ID, address) VALUES(?, ?)",
                (citizen_ID, address)
            )


        elif table_to_add.upper() == "CITIZEN_TEL":
            citizen_ID = int(input("Enter citizen ID: "))
            tel = input("Enter the telephone number of the citizen: ")

            cursor.execute(
                "INSERT OR IGNORE INTO CITIZEN_TEL(citizen_ID, tel) VALUES(?, ?)",
                (citizen_ID, tel)
            )

        elif table_to_add.upper() == "WORKS_ON":
            employee_ID = int(input("Enter the employee_ID: "))
            project_ID = int(input("Enter the project ID: "))
            start_date = input("Enter the start date: ")
            end_date = input("Enter the end date: ")

            cursor.execute(
                "INSERT OR IGNORE INTO WORKS_ON(employee_ID, project_ID, start_date, end_date) VALUES(?, ?, ?, ?)",
                (employee_ID, project_ID, start_date, end_date)
            )

        elif table_to_add.upper() == "REQUESTS":
            service_ID = int(input("Enter the service ID: "))
            citizen_ID = int(input("Enter the citizen ID: "))
            request_date = input("Enter the requested date: ")

            cursor.execute(
                "INSERT OR IGNORE INTO REQUESTS(service_ID, citizen_ID, request_date) VALUE(?, ?, ?)",
                (service_ID, citizen_ID, request_date)
            )


        elif table_to_add.upper() == "WORKS_FOR":
            employee_ID = int(input("Enter the employee ID: "))
            department_ID = int(input("Enter the department ID: "))

            cursor.execute(
                "INSERT OR IGNORE INTO WORKS_FOR(employee_ID, department_ID) VALUES(?, ?)",
                (employee_ID, department_ID)
            )

        elif table_to_add.upper() == "OFFERS":
            department_ID = int(input("Enter the department ID: "))
            service_ID = int(input("Enter the service ID: "))

            cursor.execute(
                "INSERT OR IGNORE INTO OFFERS(department_ID, service_ID) VALUES(?, ?)",
                (department_ID, service_ID)
            )

        elif table_to_add.upper() == "CONTROLS":
            department_ID = int(input("Enter the department_ID: "))
            project_ID = int(input("Enter the project_ID: "))

            cursor.execute(
                "INSERT OR IGNORE INTO CONTROLS(department_ID, project_ID) VALUES(?, ?)",
                (department_ID, project_ID)
            )

        # Commit changes to the database
        conn.commit()
        print(f"Record added to {table_to_add}.")
    except sqlite3.Error as e:
        print("Error occured while adding the record:", e)
    except ValueError as ve:
        print("Invalid input! Please try again:", ve)

add_records()
# tested on terminal and added a record of (7, "Cansu", "Abay", "cansuabay@gmail.com", 100000.00, 1001) inside the EMPLOYEE table

print()

# user deleting a record from a table
def delete_records():
    try:
        # first enter the table name to then change a record from it
        record_to_delete = input("Enter a table name to delete a record (or type 'QUIT' to quit): ").strip()
        if record_to_delete.upper() == "QUIT":
            print("Delete record function is stopped")
            return # ends the function

        # deleting a record
        if record_to_delete.upper() == "EMPLOYEE":
            employee_ID = int(input("Enter the employee ID of the record you want to delete: "))
            cursor.execute("DELETE FROM EMPLOYEE WHERE employee_ID = ?", (employee_ID,))

        elif record_to_delete.upper() == "DEPARTMENT":
            department_ID = int(input("Enter the department ID of the record you want to delete: "))
            cursor.execute("DELETE FROM DEPARTMENT WHERE department_ID = ?", (department_ID,))

        elif record_to_delete.upper() == "PROJECT":
            project_ID = int(input("Enter the project ID of the record you want to delete: "))
            cursor.execute("DELETE FROM PROJECT WHERE project_ID = ?",(project_ID,))

        elif record_to_delete.upper() == "SERVICE":
            service_ID = int(input("Enter the service_ID of the record you want to delete :"))
            cursor.execute("DELETE FROM SERVICE WHERE service_ID = ?", (service_ID,))

        elif record_to_delete.upper() == "CITIZEN":
            citizen_ID = int(input("Enter citizen ID of the record you want to delete: "))
            cursor.execute("DELETE FROM CITIZEN WHERE citizen_ID = ?", (citizen_ID,))

        elif record_to_delete.upper() == "CITIZEN_TEL":
            citizen_ID = int(input("Enter the citizen_ID of the record you want to delete: "))
            tel = input("Enter the telephone number of the record you want to delete: ")
            cursor.execute("DELETE FROM CITIZEN_TEL WHERE citizen_ID = ? AND tel = ?", (citizen_ID, tel))

        elif record_to_delete.upper() == "WORKS_ON":
            employee_ID = int(input("Enter the employee ID of the record you want to delete:"))
            project_ID = int(input("Enter the project ID of the record you want to delete: "))
            cursor.execute("DELETE FROM WORKS_ON WHERE employee_ID = ? AND project_ID = ?", (employee_ID, project_ID))

        elif record_to_delete.upper() == "REQUESTS":
            service_ID = int(input("Enter the service ID of the record you want to delete: "))
            citizen_ID = int(input("Enter the citizen ID of the record you want to delete: "))
            cursor.execute("DELETE FROM REQUESTS WHERE service_ID = ? AND citizen_ID = ?", (service_ID, citizen_ID))

        elif record_to_delete.upper() == "WORKS_FOR":
            employee_ID = int(input("Enter the employee ID of the record you want to delete: "))
            department_ID = int(input("Enter the department ID of the record you want to delete: "))
            cursor.execute("DELETE FROM WORKS_FOR WHERE employee_ID = ? AND department_ID = ?", (employee_ID, department_ID))

        elif record_to_delete.upper() == "OFFERS":
            service_ID = int(input("Enter the service ID of the record you want to delete: "))
            department_ID = int(input("Enter the department ID of the record you want to delete: "))
            cursor.execute("DELETE FROM OFFERS WHERE service_ID = ? AND department_ID = ?", (service_ID, department_ID))

        elif record_to_delete.upper() == "CONTROLS":
            department_ID = int(input("Enter the department ID of the record you want to delete: "))
            project_ID = int(input("Enter the project ID of the record you want to delete: "))
            cursor.execute("DELETE FROM CONTROLS WHERE department_ID = ? AND project_ID = ?", (department_ID, project_ID))

            # Commit changes to the database
        conn.commit()
        print(f"Record deleted from {record_to_delete}.")

    except sqlite3.Error as e:
        print("Error occured while deleting the record:", e)
    except ValueError as ve:
        print("Invalid input! Please try again:", ve)


delete_records()
# tested on terminal and deleted (7, "Cansu", "Abay", "cansuabay@gmail.com", 100000.00, 1001) that I added previously.

print()

# updating a record (2 tane yaptım)
def update_employee_records(new_email, new_employee_ID):
    try:
        # changing the email of an employee
        cursor.execute("UPDATE EMPLOYEE SET email = ? WHERE employee_ID = ?", (new_email, new_employee_ID))

        conn.commit() # commit changes
        print("Changed the email of the employee to orhandila@gmail.com who's ID is 7")
    except sqlite3.Error as e:
        print("Error occurred while updating the record:", e)

update_employee_records("orhandila@gmail.com", 6)

print()

def update_project_records(new_status, new_project_ID):
    try:
        # changing the email of an employee
        cursor.execute("UPDATE PROJECT SET status = ? WHERE project_ID = ?", (new_status, new_project_ID))

        conn.commit() # commit changes
        print("Changed the status of the project to 'Ongoing' of the project ID 13.")
    except sqlite3.Error as e:
        print("Error occurred while updating the record:", e)

update_project_records("Ongoing", 13)

print()

# join operation and getting the departments of each employee
def show_employee_departments():
    try:
        # using join with sql query
        cursor.execute('''
            SELECT EMPLOYEE.fname, EMPLOYEE.lname, DEPARTMENT.department_name
            FROM EMPLOYEE
            INNER JOIN DEPARTMENT ON EMPLOYEE.department_ID = DEPARTMENT.department_ID
        ''')

        results = cursor.fetchall()

        #displaying the results
        print("Employee Name | Department")
        print("-" * 30)
        for row in results:
            print(f"{row[0]} {row[1]} | {row[2]}")

    except sqlite3.Error as e:
        print("Error occurred while performing the join operation:", e)

show_employee_departments()

print()
print()

# displaying which services belong to which department using join
def show_services_by_department():
    try:
        cursor.execute('''
            SELECT SERVICE.service_name, DEPARTMENT.department_name
            FROM SERVICE
            INNER JOIN DEPARTMENT ON SERVICE.department_ID = DEPARTMENT.department_ID
        ''')
        results = cursor.fetchall()

        print("Service Name | Department")
        print("-" * 40)
        for row in results:
            print(f"{row[0]} | {row[1]}")

    except sqlite3.Error as e:
        print("Error occurred while performing the join operation:", e)

show_services_by_department()
























