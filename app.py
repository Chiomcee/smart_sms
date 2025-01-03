from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

    
app = Flask(__name__)
   
app.secret_key = 'chomcee1234'  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mysqlpw@232024'
app.config['MYSQL_DB'] = 'sms_users'
  
mysql = MySQL(app)


# --- Routes for User Authentication ---
@app.route('/')
@app.route('/index')
def index():
    """Route for the home page"""
    # Example current user, in production, user should be retrieved from database
    class User:
      def __init__(self, username, role, is_authenticated):
        self.username = username
        self.role = role
        self.is_authenticated = is_authenticated
    current_user = User(session.get('username'), session.get('role'), session.get('is_authenticated')) if session.get('is_authenticated') else User(None,None,False)
    return render_template('index.html', current_user=current_user) # pass current_user to the template.

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']        
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM registrations WHERE status="active" AND username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['name'] = user['first_name']
            session['username'] = user['']
            session['role'] = user['type']
            message = 'Logged in successfully !'            
            return render_template('index.html', message = message)
        else:
            message = 'Please enter correct username / password !'
    return render_template('login.html', message = message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)
    session.pop('name', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    print(request.form)
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM registrations WHERE username = %s', (username,))
            user = cursor.fetchone()
            if user:
                message = 'Account already exists!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                message = 'Username must contain only characters and numbers!'
            elif not username or not password:
                message = 'Please fill out the form!'
            else:
                try:
                    cursor.execute('INSERT INTO registrations VALUES (NULL, %s, %s)', (username, password))
                    mysql.connection.commit()
                    message = 'You have successfully registered!'
                except Exception as e:
                    message = f"An error occurred: {e}"
        else:
            message = 'Please fill all required fields!'
    return render_template('register.html', message=message)

@app.route('/add_class', methods=['GET', 'POST'])
def add_class():
    message = ''  # Initialize an empty message
    if request.method == 'POST':  # Check if the request method is POST
        print(request.form) # Print the form values for debugging
        if 'class_name' in request.form and 'teacher_id' in request.form:  # Check if required fields are present
            class_name = request.form['class_name']
            teacher_id = request.form['teacher_id']

            #Input validation
            if not class_name:
                message = 'Class name cannot be empty!'
            elif not teacher_id:
                message = 'Teacher id cannot be empty!'
            else:
                try:
                    # Connect to the database
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                    # Check if the class already exists
                    cursor.execute('SELECT * FROM classes WHERE class_name = %s', (class_name,))
                    existing_class = cursor.fetchone()
                    if existing_class:
                        message = 'Class already exists!'
                    else:
                        # Check if the teacher exists
                        cursor.execute('SELECT * FROM registrations WHERE id = %s AND type="teacher" ', 
                                    (teacher_id,))
                        if teacher_exists := cursor.fetchone():
                            try:
                                # Insert the new class into the database
                                sql = 'INSERT INTO classes VALUES (NULL, %s, %s)' 

                                message = 'Class added successfully!'
                            except Exception as e:
                                message = f'Error adding class to database: {e}'
                        else:
                            message = 'Invalid teacher id!'
                except Exception as e:
                        message = f'Error accessing database: {e}'
    else:
        message = 'Please fill all required fields' # Error message if form values are not present

    return render_template('add_class.html', message=message)


# # --- Add Student ---
# @app.route('/add_student', methods=['GET', 'POST'])
# def add_student():
#     message = ''
#     if request.method == 'POST':
#         student_name = request.form.get('student_name')
#         dob = request.form.get('dob')
#         guardian_id = request.form.get('guardian_id')
#         class_id = request.form.get('class_id')

#         if student_name and dob and guardian_id and class_id:
#             try:
#                 cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#                 cursor.execute('INSERT INTO students (name, dob, guardian_id, class_id) VALUES (%s, %s, %s, %s)',
#                                (student_name, dob, guardian_id, class_id))
#                 mysql.connection.commit()
#                 message = 'Student added successfully!'
#             except Exception as e:
#                 message = f"An error occurred: {e}"
#         else:
#             message = 'Please fill all required fields!'

#     return render_template('add_student.html', message=message)

# # --- Add Teacher ---
# @app.route('/add_teacher', methods=['GET', 'POST'])
# def add_teacher():
#     message = ''
#     if request.method == 'POST':
#         teacher_name = request.form.get('teacher_name')
#         email = request.form.get('email')
#         class_id = request.form.get('class_id')

#         if teacher_name and email:
#             try:
#                 cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#                 cursor.execute('INSERT INTO teachers (name, email, class_id) VALUES (%s, %s, %s)',
#                                (teacher_name, email, class_id))
#                 mysql.connection.commit()
#                 message = 'Teacher added successfully!'
#             except Exception as e:
#                 message = f"An error occurred: {e}"
#         else:
#             message = 'Please fill all required fields!'

#     return render_template('add_teacher.html', message=message)

# # --- Add Class ---
# @app.route('/add_class', methods=['GET', 'POST'])
# def add_class():
#     message = ''
#     if request.method == 'POST':
#         class_name = request.form.get('class_name')
#         teacher_id = request.form.get('teacher_id')

#         if class_name:
#             try:
#                 cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#                 cursor.execute('INSERT INTO classes (class_name, teacher_id) VALUES (%s, %s)',
#                                (class_name, teacher_id))
#                 mysql.connection.commit()
#                 message = 'Class added successfully!'
#             except Exception as e:
#                 message = f"An error occurred: {e}"
#         else:
#             message = 'Please fill all required fields!'

#     return render_template('add_class.html', message=message)

# # --- Edit Student ---
# @app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
# def edit_student(student_id):
#     message = ''
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('SELECT * FROM students WHERE id = %s', (student_id,))
#     student = cursor.fetchone()

#     if request.method == 'POST':
#         student_name = request.form.get('student_name')
#         dob = request.form.get('dob')
#         guardian_id = request.form.get('guardian_id')
#         class_id = request.form.get('class_id')

#         if student_name and dob and guardian_id and class_id:
#             try:
#                 cursor.execute('UPDATE students SET name=%s, dob=%s, guardian_id=%s, class_id=%s WHERE id=%s',
#                                (student_name, dob, guardian_id, class_id, student_id))
#                 mysql.connection.commit()
#                 message = 'Student updated successfully!'
#             except Exception as e:
#                 message = f"An error occurred: {e}"
#         else:
#             message = 'Please fill all required fields!'

#     return render_template('edit_student.html', message=message, student=student)

# # --- Edit Teacher ---
# @app.route('/edit_teacher/<int:teacher_id>', methods=['GET', 'POST'])
# def edit_teacher(teacher_id):
#     message = ''
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('SELECT * FROM teachers WHERE id = %s', (teacher_id,))
#     teacher = cursor.fetchone()

#     if request.method == 'POST':
#         teacher_name = request.form.get('teacher_name')
#         email = request.form.get('email')
#         class_id = request.form.get('class_id')

#         if teacher_name and email:
#             try:
#                 cursor.execute('UPDATE teachers SET name=%s, email=%s, class_id=%s WHERE id=%s',
#                                (teacher_name, email, class_id, teacher_id))
#                 mysql.connection.commit()
#                 message = 'Teacher updated successfully!'
#             except Exception as e:
#                 message = f"An error occurred: {e}"
#         else:
#             message = 'Please fill all required fields!'

#     return render_template('edit_teacher.html', message=message, teacher=teacher)

# # --- Edit Class ---
# @app.route('/edit_class/<int:class_id>', methods=['GET', 'POST'])
# def edit_class(class_id):
#     message = ''
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('SELECT * FROM classes WHERE id = %s', (class_id,))
#     class_data = cursor.fetchone()

#     if request.method == 'POST':
#         class_name = request.form.get('class_name')
#         teacher_id = request.form.get('teacher_id')

#         if class_name:
#             try:
#                 cursor.execute('UPDATE classes SET class_name=%s, teacher_id=%s WHERE id=%s',
#                                (class_name, teacher_id, class_id))
#                 mysql.connection.commit()
#                 message = 'Class updated successfully!'
#             except Exception as e:
#                 message = f"An error occurred: {e}"
#         else:
#             message = 'Please fill all required fields!'

#     return render_template('edit_class.html', message=message, class_data=class_data)

# # --- Pay Fees ---
# @app.route('/pay_fees', methods=['GET', 'POST'])
# def pay_fees():
#     message = ''
#     if request.method == 'POST':
#         student_id = request.form.get('student_id')
#         amount_paid = request.form.get('amount_paid')
#         payment_date = request.form.get('payment_date')

#         if student_id and amount_paid and payment_date:
#             try:
#                 cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#                 cursor.execute('INSERT INTO fees (student_id, amount_paid, payment_date, status) VALUES (%s, %s, %s, "Paid")',
#                                (student_id, amount_paid, payment_date))
#                 mysql.connection.commit()
#                 message = 'Payment recorded successfully!'
#             except Exception as e:
#                 message = f"An error occurred: {e}"
#         else:
#             message = 'Please fill all required fields!'

#     return render_template('pay_fees.html', message=message)

# # --- Notifications ---
# @app.route('/notification', methods=['GET', 'POST'])
# def notification():
#     message = ''
#     if request.method == 'POST':
#         user_id = request.form.get('user_id')
#         message_content = request.form.get('message')

#         if user_id and message_content:
#             try:
#                 cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#                 cursor.execute('INSERT INTO notifications (user_id, message, status) VALUES (%s, %s, "Sent")',
#                                (user_id, message_content))
#                 mysql.connection.commit()
#                 message = 'Notification sent successfully!'
#             except Exception as e:
#                 message = f"An error occurred: {e}"
#         else:
#             message = 'Please fill all required fields!'

#     return render_template('notification.html', message=message)


# if __name__ == '__main__':
#     app.debug = True
#     app.run()
