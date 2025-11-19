import sqlite3
from datetime import datetime 

# -------------- CONNECTION TO DATABASE ----------------

conn = sqlite3.connect('employee_managment.db')
cursor = conn.cursor()
print('✅ Database connected successfully')


#-------------------CREATE TABLES ---------------------

# == TABLE FOR USER ==
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE,
               password TEXT)
    ''')

# == TABLE FOR MANGER ==
cursor.execute('''
    CREATE TABLE IF NOT EXISTS manager(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
            )           
    ''')

# == TABLE FOR DEPARTMENT ==
cursor.execute('''
    CREATE TABLE IF NOT EXISTS department (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT )
                                    
''')                    

# == TABLE FOR EMPLOYEE ==
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,       
        position TEXT,       
        department_id INTEGER,
        manager_id INTEGER,
        salary INTEGER,
        date_joined TEXT,              
        FOREIGN KEY (department_id) REFERENCES department (id) ,
        FOREIGN KEY (manager_id) REFERENCES manager(id)     )                                                                                
''')

# == TABLE FOR LEAVE RECORD ==
cursor.execute('''
    CREATE TABLE IF NOT EXISTS leave_record(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        leave_type TEXT,
        start_date TEXT,
        end_date TEXT,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY (employee_id) REFERENCES employee (id)  )
''')       
                                                                                                                                               
conn.commit()
print('✅ Tables created successfully.')

#-----------------USER AUTHENTICATION--------------------

def register_user(username, password):
    "Registers a new system user."
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)' ,(username, password))
        conn.commit()
        print('✅ user registered successfully.')
    except sqlite3.IntegrityError:
        print('🙏Username already exists. Please choose another.')
    except sqlite3.Error as e:
        print ('❌ Error registering user:',e)

def login_user(username, password):
    'Validates login credentials.'
    try:
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?',(username, password))
        user = cursor.fetchone()
        if user:
            print(f'Welcome, {username} !')
            return True
        else:
            print('⚠️ Invalid username or password.')
            return False
    except sqlite3.Error as e:
        print('❌ Error during login:', e)
        return False




#  -----------DEPARTMENT / MANAGER------------------------

# ADD DEPARTMENT
def add_department(name):
    try:
        cursor.execute('INSERT INTO department (name) VALUES (?)', (name,))
        conn.commit()
        print('✅ Department added successfully.')
    except sqlite3.Error as e:
        print('❌ Error adding department:', e) 

# ADD MANAGER
def add_manager(name):
    try: 
        cursor.execute('INSERT INTO manager (name) VALUES (?)' , (name,))
        conn.commit()
        print('✅ Manager added successfully.')
    except sqlite3.Error as e:
        print('❌ Error adding manager:', e)    
 

#-------------- EMPLOYEE -------------

# ADD EMPLOYEE 
def add_employee(name, position, department_id, manager_id, salary):
    try:
        date_joined = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO employee (name, position, department_id, manager_id, salary, date_joined)
            VALUES (?, ?, ?, ?, ?, ?) 
        ''', (name,position, department_id, manager_id, salary, date_joined) )
        conn.commit()
        print(f" ✅ Employee '{name}' added successfully.")
    except sqlite3.Error as e:
        print('❌ Error adding Employee:', e)   

# VIEW EMPLOYEE
def view_employee():
    try:
        cursor.execute('''
            SELECT e.id, e.name, e.position, d.name AS department,m.name AS manager, e.salary, e.date_joined    
            FROM employee e
            LEFT JOIN department d ON e.department_id = d.id   
            LEFT JOIN manager m ON e.manager_id = m.id
            ORDER BY e.id                                               
        ''')
        rows = cursor.fetchall()
        if not rows:
            print('❌ No employee found.')
        else:
             print("\n========== EMPLOYEE LIST ==========")
             for row in rows:
                print(f"""
          ID: {row[0]}
          Name: {row[1]}
          Position: {row[2]}
          Department: {row[3]}
          Manager: {row[4]}
          Salary: {row[5]}
          Date Joined: {row[6]}
---------------------------------------
""")
    except sqlite3.Error as e:
        print('❌ Error viewing employee:', e)


# UPDATE EMPLOYEE
def update_employee_salary(emp_id, new_salary):
    try:    
        cursor.execute('UPDATE employee SET salary=? WHERE id=?', (new_salary,emp_id))      
        conn.commit()
        if cursor.rowcount:
             print('💰 Employee salary updated.')
        else:
            print('No employee found with that ID.')     
    except sqlite3.Error as e:
        print('❌ Error updating salary:', e)
           

# DELETE EMPLOYEE
def delete_employee(emp_id):
    try:
        cursor.execute('DELETE FROM employee WHERE id=?', (emp_id,))
        conn.commit()
        if cursor.rowcount:
            print('🗑️ Employee deleted.')
        else:
            print('🙏 No employee found with that ID.')
    except sqlite3.Error as e:
        print('❌ Error deleting employee:', e)            


# APPLY LEAVE
def apply_leave(employee_id, leave_type, start_date, end_date):
    try:
        cursor.execute('''
            INSERT INTO leave_record (employee_id, leave_type, start_date, end_date)
            VALUES (?, ?, ?, ?)
        ''', (employee_id, leave_type, start_date, end_date))
        conn.commit()
        print('📆 Leave applied successfully.')
    except sqlite3.Error as e:
        print('❌ Error applying leave:', e)   



def view_leaves():
    cursor.execute('''
         SELECT l.id, e.name, l.leave_type, l.start_date, l.end_date, l.status
         FROM leave_record l
         JOIN employee e ON l.employee_id = e.id 
         ORDER BY l.id
    ''') 

    rows = cursor.fetchall()

    if not rows:
        print('❌ No leave records found.')
        return

    print("\n=== LEAVE RECORDS ===")
    for row in rows:
        print(f"""
---------------------------------------------
          ID:          {row[0]}
          Name:        {row[1]}
          Leave Type:  {row[2]}
          Start Date:  {row[3]}
          End Date:    {row[4]}
          Status:      {row[5]}
---------------------------------------------
""")

                
# UPDATE LEAVE                
def update_leave_status(leave_id, new_status):
    try:
        cursor.execute('UPDATE leave_record SET status=? WHERE id=?', (new_status, leave_id) )
        conn.commit()
        if cursor.rowcount:
            print('✅ Leave status updated.')
        else:
            print('No leave record found with that ID.')
    except sqlite3.Error as e:
        print('❌ Error updating leave status:', e)            


# FILTER BY ROLE
def filter_by_role(position_title):
    cursor.execute('''
        SELECT id, name, position, salary
        FROM employee 
        WHERE position = ?           
    ''', (position_title,)) 
    rows = cursor.fetchall()
    if not rows:
        print('❌ No employee with that position found.')
    else:
        print("\n ====== Role ======")
        for row in rows:
            print(f"""
------------------------------------------                  
             ID: {row[0]}
             Name: {row[1]}
             Position: {row[2]}
             Salary: {row[3]}
------------------------------------------
                  """)

# FILTER BY DEPARTMENT
def filter_by_department(dept_name):
    try:
        cursor.execute('''
            SELECT e.id, e.name, e.position, d.name
            FROM employee e
            JOIN department d ON e.department_id = d.id           
            WHERE d.name=?           
        ''', (dept_name,)) 
        rows = cursor.fetchall()
        if not rows:
            print('No employee found in that department.')
        else:
             print("\n   ===== Department ======    ") 
             for row in rows:
               print(f"""
------------------------------------------------------                     
               ID: {row[0]}
               Employee Name: {row[1]}
               Position: {row[2]}
               Department Name: {row[3]}
------------------------------------------------------- 
""")  
    except sqlite3.Error as e:
        print('❌ Error filtering by department:', e)        


# FILTER LEAVE STATUS
def filter_leaves_by_status(status):
    cursor.execute('''
        SELECT l.id, e.name, l.leave_type, l.start_date, l.end_date, l.status
        FROM leave_record l
        JOIN employee e ON l.employee_id = e.id
        WHERE l.status=?           
    ''', (status,))
    
    rows = cursor.fetchall()
    
    if not rows:
        print("❌ No leaves found with that status.")
        return
    
    print(f"\n========== LEAVES WITH STATUS: {status.upper()} ==========")
    
    for row in rows:   
        print(f"""
---------------------------------------------
          ID:          {row[0]}
          Name:        {row[1]}
          Leave Type:  {row[2]}
          Start Date:  {row[3]}
          End Date:    {row[4]}
          Status:      {row[5]}
---------------------------------------------
""")


# TOTAL SALARY               
def total_salary():
    try:
       cursor.execute('SELECT SUM(salary) FROM employee')
       total = cursor.fetchone()[0]
       print('💰 Total Salary: ', total if total else 0)
    except sqlite3.Error as e:
        print('❌ Error calculating total salary:', e)


# JOINING DATE
def list_by_joining_date(): 
    cursor.execute('SELECT name, date_joined FROM employee ORDER BY date_joined ') 
    print("\n ======= Joined Date ======")
    for row in cursor.fetchall():
        print (f"""
-----------------------------------
          Name = {row[0]}
          Date Joined = {row[1]}
------------------------------------
""")


#------------------MAIN MENU --------------------------

def main_menu():
    while True:
        print('\n  🔷 EMPLOYEE MANAGMENT SYSTEM 🔷 ')
        print('1. Add Department')
        print('2. Add Manager')
        print('3. Add Employee')
        print('4. View Employee')
        print('5. Update employee Salary')
        print('6. Delete Employee')
        print('7. Filter by Department')   
        print('8. Filter by Role (position text)')                         
        print('9. Total Salary')             
        print('10. List by Joining Date')
        print('11. Apply Leave')
        print('12. View Leave')                                                       
        print('13. Update Leave Status')     
        print('14. Filter Leaves by Status')   
        print('0. Exit')


        choice = input('Enter choice: ')

        try:
            if choice == '1' :
                add_department(input('Department Name: '))
            elif choice == '2' :
                add_manager(input('Manager Name: '))
            elif choice == '3' :
                add_employee(
                input('Employee Name: '),
                input('Position : ') ,
                int(input('Department ID: ') ),
                int(input('Manager ID: ')) ,
                int(input('Salary: '))
                )
            elif choice == '4' :
                view_employee()
            elif choice == '5' :
                update_employee_salary(int(input('Employee ID: ')), int(input('New Salary: ')))
            elif choice == '6' :
                delete_employee(int(input('Employee ID: '))) 
            elif choice == '7' :
                filter_by_department(input('Department Name: '))
            elif choice == '8' :
                filter_by_role(input('Position Title: '))
            elif choice == '9' :
                total_salary()
            elif choice == '10' :
                list_by_joining_date()
            elif choice == '11' :
                apply_leave(
                    int(input('Employee ID: ')),
                    input('Leave Type: '),
                    input('Start Date (YYYY-MM-DD): '),
                    input('End Date (YYYY-MM-DD): ')
                )                        
            elif choice == '12' :
                view_leaves()
            elif choice == '13' :
                update_leave_status(int(input('Leave ID: ')), input('New Status (Approved/Rejected): '))
            elif choice == '14' :
                filter_leaves_by_status(input('Status (pending/Approved/Rejected): '))
            elif choice == '0' :
                print('👋 Exitig program...')
                break
            else:
                print('⚠️ Invalid choice. Try again.')
        except Exception as e:
            print('Error:', e)
    


#------------ LOGIN MENU ----------------
 
def login_menu():
    while True:
        print('\n 🔷 LOGIN MENU 🔷')
        print('1️⃣ Register User ')
        print('2️⃣ Login ')
        print('0️⃣ Exit ')

        choice = input('Enter choice: ')

        if choice == '1':
            register_user(input('Username: '), input('Password: '))
        elif choice == '2':
            if login_user(input('Username: '), input('Password: ')):
                main_menu()
        elif choice == '0':
            print('👋Exiting program...')  
            break
        else:
            print('⚠️ Invalid choice. Try again.')



if __name__=='__main__':
    try:
        login_menu()

    finally:    
        conn.close()
        print ('❌ Database connection closed.')
             