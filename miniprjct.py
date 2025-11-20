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
               password TEXT,
               role TEXT )
    ''')

# == TABLE FOR MANGER ==
cursor.execute('''
    CREATE TABLE IF NOT EXISTS manager(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT)           
    ''')

# == TABLE FOR DEPARTMENT ==
cursor.execute('''
    CREATE TABLE IF NOT EXISTS department (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE)
                                    
''')                    

# == TABLE FOR EMPLOYEE ==
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,       
        name TEXT,       
        position TEXT,       
        department_id INTEGER,
        manager_id INTEGER,
        salary INTEGER,
        date_joined TEXT,              
        FOREIGN KEY (user_id) REFERENCES users (id) ,
        FOREIGN KEY (department_id) REFERENCES department (id),
        FOREIGN KEY (manager_id) REFERENCES manager (id) )        
                                                                                       
''')

# == TABLE FOR LEAVE RECORD ==
cursor.execute('''
    CREATE TABLE IF NOT EXISTS leave_record(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        leave_type TEXT,
        start_date TEXT,
        end_date TEXT,
        status TEXT ,
        FOREIGN KEY (employee_id) REFERENCES employee (id)  )
''')       
                                                                                                                                               
conn.commit()
print('✅ Tables created successfully.')


#---------- HELPERS ----------
def input_nonempty(prompt):
    while True:
        v = input(prompt).strip()
        if v != '':
            return v
        print("⚠️ Input cannot be empty.")

def input_int(prompt, allow_empty=False, default=None):
    while True:
        v = input(prompt).strip()
        if v == '' and allow_empty:
            return default
        try:
            return int(v)
        except ValueError:
            print("⚠️ Please enter a valid integer.")

def ensure_defaults():
    # default admin
    cursor.execute("SELECT id FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ('admin', 'admin123', 'employer'))
    # sample department and manager
    cursor.execute("SELECT id FROM department")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO department (name) VALUES (?)", ("General",))
    cursor.execute("SELECT id FROM manager")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO manager (name) VALUES (?)", ("Default Manager",))
    conn.commit()
def list_departments():
    cursor.execute("SELECT id, name FROM department ORDER BY id")
    rows = cursor.fetchall()
    if not rows:
        print("No departments.")
    else:
        print("\nDepartments:")
        for r in rows:
            print(f"  {r[0]} - {r[1]}")

def list_managers():
    cursor.execute("SELECT id, name FROM manager ORDER BY id")
    rows = cursor.fetchall()
    if not rows:
        print("No managers.")
    else:
        print("\nManagers:")
        for r in rows:
            print(f"  {r[0]} - {r[1]}")

def list_users():
    cursor.execute("SELECT id, username, role FROM users ORDER BY id")
    rows = cursor.fetchall()
    if not rows:
        print("No users.")
    else:
        print("\nUsers:")
        for r in rows:
            print(f"  {r[0]} - {r[1]} ({r[2]})")

ensure_defaults()


# ------------------- USER REGISTRATION -------------------
def register_user():
    username = input('Username: ')
    password = input('Password: ')
    role = input('Role (employer/employee): ').lower()
    if role not in ('employer', 'employee'):
        print("❌ Role must be 'employer' or 'employee' .")
        return
    try:
        cursor.execute('INSERT INTO users(username, password, role) VALUES (?,?,?)',
        (username, password, role))
        conn.commit()
        print("✅ User Registered Successfully")
    except sqlite3.IntegrityError:
        print("❌ Username Already Exists")


# ------------------- LOGIN -------------------
def login():
    username = input_nonempty('Username: ')
    password = input_nonempty('Password: ')
    cursor.execute('SELECT id, role FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    if user:
        uid, role = user
        print(f"\n🔐 Login Success! Welcome {username} ({role})\n")
        return uid, role, username
    else:
        print("❌ Invalid Login")
        return None

#  -----------DEPARTMENT / MANAGER------------------------

# ADD DEPARTMENT
def add_department():
    name = input('Department name : ')
    try:
        cursor.execute('INSERT INTO department (name) VALUES (?)', (name,))
        conn.commit()
        print('✅ Department added successfully.')
    except sqlite3.Error as e:
        print('❌ Department Already Exist! ')


# ADD MANAGER
def add_manager():
        name = input('Manager Name: ') 
        cursor.execute('INSERT INTO manager (name) VALUES (?)' , (name,))
        conn.commit()
        print('✅ Manager added successfully.')
      

#-------------- EMPLOYEE FUNCTIONS -------------

# ---------- EMPLOYEE ----------
def add_employee():
    print("Link Employee User Account")
    username = input_nonempty("Enter employee username: ")

    # fetch id and role (fixed: select id and role)
    cursor.execute("SELECT id, role FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if not user:
        print("❌ No such user. Register the user first.")
        return
    user_id, user_role = user
    if user_role != 'employee':
        print("❌ This user is not registered as role 'employee'. Change role or register a proper user.")
        return

    name = input_nonempty('Employee Name: ')
    position = input_nonempty('Position: ')

    # show departments/managers for convenience
    list_departments()
    dept_id = input_int('Department ID (or press Enter to create new): ', allow_empty=True, default=None)
    if dept_id is None:
        new_dept = input_nonempty('New Department name: ')
        try:
            cursor.execute("INSERT INTO department (name) VALUES (?)", (new_dept,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        cursor.execute("SELECT id FROM department WHERE name=?", (new_dept,))
        dept_id = cursor.fetchone()[0]

    list_managers()
    manager_id = input_int('Manager ID (or press Enter to create new): ', allow_empty=True, default=None)
    if manager_id is None:
        new_mgr = input_nonempty('New Manager name: ')
        cursor.execute("INSERT INTO manager (name) VALUES (?)", (new_mgr,))
        conn.commit()
        cursor.execute("SELECT id FROM manager WHERE name=?", (new_mgr,))
        manager_id = cursor.fetchone()[0]

    salary = input_int('Salary: ')
    date_joined = datetime.now().strftime('%Y-%m-%d')

    cursor.execute('''
        INSERT INTO employee (user_id, name, position, department_id, manager_id, salary, date_joined)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, name, position, dept_id, manager_id, salary, date_joined))
    conn.commit()
    print(f"✅ Employee '{name}' added successfully and linked to user '{username}' (user_id={user_id}).")



    
     
# VIEW EMPLOYEE
def view_employee():
    try:
        cursor.execute(''' SELECT e.id, e.name, e.position, d.name AS department,m.name AS manager, e.salary, e.date_joined
                         FROM employee e
                         LEFT JOIN department d ON e.department_id = d.id
                         LEFT JOIN manager m ON e.manager_id = m.id
                         ORDER BY e.id ''') 
        rows = cursor.fetchall()
        if not rows:
             print('❌ No employee found.')
        else:
            print("\n========== EMPLOYEE LIST ==========")
            for row in rows:
             print(f""" 
    -------------------------------------------               
             ID:          {row[0]} 
             Name:        {row[1]} 
             Position:    {row[2]} 
             Department:  {row[3]} 
             Manager:     {row[4]} 
             Salary:      {row[5]} 
             Date Joined: {row[6]} 
    ------------------------------------------- """)
    except sqlite3.Error as e:
            print('❌ Error viewing employee:', e)
    
# UPDATE EMPLOYEE
def update_employee_salary():
    try: 
        emp_id = int(input('Employee ID: '))
        new_salary = int(input('New Salary: '))   
        cursor.execute('UPDATE employee SET salary=? WHERE id=?', (new_salary,emp_id))      
        conn.commit()
        if cursor.rowcount:
             print('💰 Employee salary updated.')
        else:
            print('No employee found with that ID.')     
    except sqlite3.Error as e:
        print('❌ Error updating salary:', e)
           

# DELETE EMPLOYEE
def delete_employee():
    try:
        emp_id =int(input('Employee ID: '))
        cursor.execute('DELETE FROM employee WHERE id=?', (emp_id,))
        conn.commit()
        if cursor.rowcount:
            print('🗑️ Employee deleted.')
        else:
            print('🙏 No employee found with that ID.')
    except sqlite3.Error as e:
        print('❌ Error deleting employee:', e)            


# ------------- --------------------------------
def view_my_profile(user_id):
    cursor.execute('SELECT name, position, salary, date_joined FROM employee WHERE user_id=?', (user_id,))
    row = cursor.fetchone()
    if not row:
        print("❌ No employee profile linked to this user.")
        return
    print(f"""
========= MY PROFILE ========
          Name:  {row[0]}
          Position : {row[1]}
          Salary : {row[2]}
          Date Joined : {row[3]}

          """)


def apply_leave(user_id):
    # find employee id user_id
    cursor.execute('SELECT id FROM employee WHERE user_id=?', (user_id,))
    emp = cursor.fetchone()
    if not emp:
        print('Not linked to employee record')
        return
    emp_id = emp[0]
    leave = input('Leave Type: ')
    start = input('start Date (YYYY-MM-DD): ')
    end = input('End Date (YYYY-MM-DD): ')

    cursor.execute('''
            INSERT INTO leave_record (employee_id, leave_type, start_date, end_date,status)
            VALUES (?, ?, ?, ?, ?)
        ''', (emp_id, leave, start, end, 'pending' ))
    conn.commit()
    print('📆 Leave applied successfully.')


def view_leave():  
    cursor.execute('''
        SELECT l.id, e.name, l.leave_type, l.start_date, l.end_date, l.status
        FROM leave_record l
        JOIN employee e ON l.employee_id = e.id 
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
    
# VIEW LEAVE

def view_my_leave(user_id):
    cursor.execute('''
        SELECT l.id, l.leave_type, l.start_date, l.end_date, l.status
        FROM leave_record l
        JOIN employee e ON l.employee_id = e.id
        WHERE e.user_id=?
        ORDER BY l.id
    ''', (user_id,))
    rows = cursor.fetchall()

    if not rows:
        print('❌ No leave records found.')
        return

    print("\n=== MY LEAVE RECORDS ===")
    for row in rows:
        print(f"""
---------------------------------------------
          ID:         {row[0]}
          Leave Type: {row[1]}
          Start Date: {row[2]}
          End Date:   {row[3]}
          Status:     {row[4]}
              
---------------------------------------------
""")

                
#  UPDATE LEAVE (admin)               
def update_leave_status():
    leave_id = int(input('Leave ID: '))
    new_status = input('New Status (approved/rejected/pending): ')
    try: 
        cursor.execute('UPDATE leave_record SET status=? WHERE id=?', (new_status, leave_id ))
        conn.commit()
        if cursor.rowcount:
          print('✅ Leave status updated.')
        else:
            print("❌ No leave record found with that ID.")           
    except sqlite3.Error as e :
     print("❌ Error updating leave status:", e)
# --------------------- FILTER FUNCTION -------------------------------
# FILTER BY ROLE
def filter_by_role():
    position_title = input('Enter position title: ')
    cursor.execute('''
        SELECT id, name, position, salary
        FROM employee 
        WHERE position = ?           
    ''', (position_title,)) 
    rows = cursor.fetchall()
    if not rows:
        print('❌ No employee with that position found.')
    else:
        print("\n ====== EMPLOYEES BY ROLE ======")
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
def filter_by_department():
    dept_name = input('Enter department name: ')
    try:
        cursor.execute('''
            SELECT e.id, e.name, e.position, d.name, e.salary
            FROM employee e
            JOIN department d ON e.department_id = d.id           
            WHERE d.name=?           
        ''', (dept_name,)) 
        rows = cursor.fetchall()
        if not rows:
            print('No employee found in that department.')
        else:
             print("\n   ===== EMPLOYEES BY DEPARTMENT ======    ") 
             for row in rows:
               print(f"""
------------------------------------------------------                     
               ID:              {row[0]}
               Employee Name:   {row[1]}
               Position:        {row[2]}
               Department Name: {row[3]}
               Salary:          {row[4]}
------------------------------------------------------- 
""")  
    except sqlite3.Error as e:
        print('❌ Error filtering by department:', e)        


# ----------------- REPORT FUNCTION -----------------
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

def employer_menu(user_id,username):
    while True:
            print(f"""

 =============== EMPLOYER MENU ================ 
                                              
 Logged in as: {username}

             
1. Add Department
2. Add Manager
3. Add Employee
4. View Employee
5. Update employee Salary
6. Delete Employee
7. View All Leaves
8. Update Leave Status                                                     
9. Filter by Department   
10. Filter by Role (position text)      
11. Total Salary
12. list by joining date                                                      
0. Logout
                  """)


            choice = input('Enter choice: ')

        
            if choice == '1' :
                add_department()
            elif choice == '2':
                add_manager()
            elif choice == '3':
                add_employee()
            elif choice == '4' :
                view_employee()
            elif choice == '5' :
                update_employee_salary()
            elif choice == '6' :
                delete_employee() 
            elif choice == '7' :
                view_leave()  
            elif choice == '8' :
                update_leave_status()      
            elif choice == '9' :
                filter_by_department()
            elif choice == '10' :
                filter_by_role()
            elif choice == '11' :
                total_salary()
            elif choice == '12' :
                list_by_joining_date()
            elif choice == '0' :
                break
            else:
                print('Invalid')


def employee_menu(user_id,username):
    while True:
        print("""
 =============== EMPLOYEE MENU ==================             
    1. View My Profile
    2. Apply Leaves
    3. View My Leaves          
    0. Logout 
              """)
        choice = input("Enter Choice: ")
        if choice == '1':
            view_my_profile(user_id)
        elif choice == '2' :
            apply_leave(user_id)
        elif choice == '3' :
            view_my_leave(user_id)
        elif choice == '0' :
            break
        else:
            print('Invalid')

def main():
    print("\n ========== EMPLOYEE MANAGEMENT SYSTEM ==========")
    while True:
         
        print("""
1. Register
2. Login
3. Exit
              """)
        
        choice = input('Choice: ')
        if choice == '1' :
            register_user()
        elif choice == '2':
            res = login()
            if res:
                uid, role, username = res
                if role == 'employer':
                    employer_menu(uid, username)
                else:
                    employee_menu(uid,username)            
        elif choice == '3':
            break
        else:
            print("❌ Invalid choice")
    print('Exiting....')

    conn.close()        


if __name__ == '__main__':
    main()
        