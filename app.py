import os
from datetime import datetime
import sqlite3
from datetime import date
from flask import Flask,request,render_template


#### Defining Flask App
app = Flask(__name__)


#### check if static folder and database folder exists or not
if not os.path.exists('static'):
    os.makedirs('static')

if not os.path.exists('database'):
    os.makedirs('database')

###### sqlite 3 code #######

conn = sqlite3.connect('database/schedular.db',check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS faculty(
            first_name text,
            last_name text,
            dob date,
            phone_number integer,
            address integer text,
            faculty_id integer text,
            password integer text,
            department text,
            status integer
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS student(
            first_name text,
            last_name text,
            dob date,
            phone_number integer,
            password integer text,
            address integer text,
            status integer
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS superusercreds(
            username integer text,
            password integer text
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS facultyappointmentrequests(
            facultyid integer text,
            studentname integer text,
            studentnum integer text,
            appointmentdate date
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS facultyappointments(
            facultyid integer text,
            studentname integer text,
            studentnum integer text,
            appointmentdate date
            )''')


###############################
c.execute('SELECT * from superusercreds')
conn.commit()
adminuser = c.fetchall()
if not adminuser:
    c.execute("INSERT INTO superusercreds VALUES ('admin','admin')")
    conn.commit()

# c.execute('SELECT * FROM id_and_password')
# c.execute("INSERT INTO id_and_password VALUES ('{}','{}','{}','{}','{}','{}')".format(ent3.get(), ent4.get(),ent5.get(), ent0.get(),ent1.get(), ent2.get()))
# c1.execute('DELETE FROM count')
# c.execute("UPDATE id_and_password SET user_id=(?) WHERE user_id=(?)",(eee4.get(),c3[0][0]))

###########################
def datetoday():
    today = datetime.now().strftime("%Y-%m-%d")
    return today

def checkonlyalpha(x):
    return x.isalpha()

def checkonlynum(x):
    return x.isdigit()

def checkpass(x):
    f1,f2,f3 = False,False,False
    if len(x)<8:
        return False
    if any(c.isalpha() for c in x):
        f1 = True
    if any(c.isdigit() for c in x):
        f2 = True
    if any(c in x for c in ['@','$','!']):
        f3 = True

    return f1 and f2 and f3

def checkphnlen(x):
    return len(x)==10

def retallfacultyandapps():
    c.execute(f"SELECT * FROM facultyappointments")
    conn.commit()
    facultyandapps = c.fetchall()
    l = len(facultyandapps)
    return facultyandapps,l

def getstudetails(phn):
    c.execute(f"SELECT * FROM student")
    conn.commit()
    student = c.fetchall()
    for i in student:
        if str(i[3])==str(phn):
            return i

def getfacdetails(facultyid):
    c.execute(f"SELECT * FROM faculty")
    conn.commit()
    faculty = c.fetchall()
    for i in faculty:
        if str(i[5])==str(facultyid):
            return i


def retfacultyandapps(facultyid):
    c.execute(f"SELECT * FROM facultyappointments")
    conn.commit()
    facultyandapps = c.fetchall()
    facultyandapps2 = []
    for i in facultyandapps:
        if str(i[0])==str(facultyid):
            facultyandapps2.append(i)
    l = len(facultyandapps2)
    return facultyandapps2,l

def retapprequests(facultyid):
    c.execute(f"SELECT * FROM facultyappointmentrequests")
    conn.commit()
    appreq = c.fetchall()
    appreq2 = []
    for i in appreq:
        if str(i[0])==str(facultyid):
            appreq2.append(i)
    l = len(appreq2)
    return appreq,l

def ret_student_reg_requests():
    c.execute('SELECT * FROM student')
    conn.commit()
    data = c.fetchall()
    student_reg_requests = []
    for d in data:
        if str(d[-1])=='0':
            student_reg_requests.append(d)
    return student_reg_requests

def ret_faculty_reg_requests():
    c.execute('SELECT * FROM faculty')
    conn.commit()
    data = c.fetchall()
    faculty_reg_requests = []
    for d in data:
        if str(d[-1])=='0':
            faculty_reg_requests.append(d)
    return faculty_reg_requests

def ret_registered_student():
    c.execute('SELECT * FROM student')
    conn.commit()
    data = c.fetchall()
    registered_student = []
    for d in data:
        if str(d[-1])=='1':
            registered_student.append(d)
    return registered_student

def ret_registered_faculty():
    c.execute('SELECT * FROM faculty')
    conn.commit()
    data = c.fetchall()
    registered_faculty = []
    for d in data:
        if str(d[-1])=='1':
            registered_faculty.append(d)
    return registered_faculty

def ret_facname_facdept():
    c.execute('SELECT * FROM faculty')
    conn.commit()
    registered_faculty = c.fetchall()
    facname_facultyid = []
    for i in registered_faculty:
        facname_facultyid.append(str(i[0])+' '+str(i[1])+'-'+str(i[5])+'-'+str(i[7]))
    l = len(facname_facultyid)
    return facname_facultyid,l

def getfacname(facultyid):
    c.execute('SELECT * FROM faculty')
    conn.commit()
    registered_faculty = c.fetchall()
    for i in registered_faculty:
        if str(i[5])==str(facultyid):
            return i[0]+'-'+i[1]

def getstuname(stunum):
    c.execute('SELECT * FROM student')
    conn.commit()
    details = c.fetchall()
    for i in details:
        if str(i[3])==str(stunum):
            return i[0]+' '+i[1]
    else:
        return -1

def get_all_facultyids():
    c.execute('SELECT * FROM faculty')
    conn.commit()
    registered_faculty = c.fetchall()
    facultyids = []
    for i in registered_faculty:
        facultyids.append(str(i[5]))
    return facultyids


def get_all_stunums():
    c.execute('SELECT * FROM student')
    conn.commit()
    registered_student = c.fetchall()
    stunums = []
    for i in registered_student:
        stunums.append(str(i[3]))
    return stunums


################## ROUTING FUNCTIONS #########################

#### Our main page
@app.route('/')
def home():
    return render_template('home.html') 


@app.route('/stureg')
def patreg():
    return render_template('studentregistration.html') 


@app.route('/facreg')
def facreg():
    return render_template('facultyregistration.html') 


@app.route('/loginpage1')
def loginpage1():
    return render_template('loginpage1.html') 


@app.route('/loginpage2')
def loginpage2():
    return render_template('loginpage2.html') 


@app.route('/loginpage3')
def loginpage3():
    return render_template('loginpage3.html') 


### Functions for adding student
@app.route('/addstudent',methods=['POST'])
def addstudent():
    passw = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    dob = request.form['dob']
    phn = request.form['phn']
    address = request.form['address']
    print(firstname,lastname,checkonlyalpha(firstname),checkonlyalpha(lastname))

    if (not checkonlyalpha(firstname)) | (not checkonlyalpha(lastname)):
        return render_template('home.html',mess=f'First Name and Last Name can only contain alphabets.')

    if not checkpass(passw):
        return render_template('home.html',mess=f"Password should be of length 8 and should contain alphabets, numbers and special characters ('@','$','!').") 

    if not checkphnlen(phn):
        return render_template('home.html',mess=f"Phone number should be of length 10.") 

    if str(phn) in get_all_stunums():
        return render_template('home.html',mess=f'Student with mobile number {phn} already exists.') 
    c.execute(f"INSERT INTO student VALUES ('{firstname}','{lastname}','{dob}','{phn}','{passw}','{address}',0)")
    conn.commit()
    return render_template('home.html',mess=f'Registration Request sent to Super Admin for Patient {firstname}.') 


### Functions for adding faculty
@app.route('/addfaculty',methods=['GET','POST'])
def addfaculty():
    passw = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    dob = request.form['dob']
    phn = request.form['phn']
    address = request.form['address']
    facultyid = request.form['facultyid']
    dept = request.form['department']
    
    if not checkonlyalpha(firstname) and not checkonlyalpha(lastname):
        return render_template('home.html',mess=f'First Name and Last Name can only contain alphabets.')

    if not checkonlyalpha(dept):
        return render_template('home.html',mess=f'Doctor department can only contain alphabets.')

    if not checkpass(passw):
        return render_template('home.html',mess=f"Password should be of length 8 and should contain alphabets, numbers and special characters ('@','$','!').") 
    
    if not checkphnlen(phn):
        return render_template('home.html',mess=f"Phone number should be of length 10.") 

    if str(facultyid) in get_all_facultyids():
        return render_template('home.html',mess=f'Faculty with fac ID {facultyid} already exists.') 
    c.execute(f"INSERT INTO faculty VALUES ('{firstname}','{lastname}','{dob}','{phn}','{address}','{facultyid}','{passw}','{dept}',0)")
    conn.commit()
    return render_template('home.html',mess=f'Registration Request sent to Super Admin for Doctor {firstname}.') 


## Patient Login Page
@app.route('/studentlogin',methods=['GET','POST'])
def studentlogin():
    phn = request.form['phn']
    passw = request.form['pass']
    c.execute('SELECT * FROM student')
    conn.commit()
    registerd_student = c.fetchall()
    for i in registerd_student:
        if str(i[3])==str(phn) and str(i[4])==str(passw):
            facultyandapps,l = retallfacultyandapps()
            facname_facultyid,l2 = ret_facname_facdept()
            facnames = []
            for i in facultyandapps:
                facnames.append(getfacname(i[0]))
            return render_template('studentlogin.html',facultyandapps=facultyandapps,facnames=facnames,facname_facultyid=facname_facultyid,l=l,l2=l2,stuname=i[1],phn=phn) 

    else:
        return render_template('loginpage1.html',err='Please enter correct credentials...')


## Doctor Login Page
@app.route('/facultylogin',methods=['GET','POST'])
def facultylogin():
    facultyid = request.form['facultyid']
    passw = request.form['pass']
    c.execute('SELECT * FROM faculty')
    conn.commit()
    registerd_faculty = c.fetchall()

    for i in registerd_faculty:
        if str(i[5])==str(facultyid) and str(i[6])==str(passw):
            appointment_requests_for_this_faculty,l1 = retapprequests(facultyid)
            fix_appointment_for_this_faculty,l2 = retfacultyandapps(facultyid)
            return render_template('facultylogin.html',appointment_requests_for_this_faculty=appointment_requests_for_this_faculty,fix_appointment_for_this_faculty=fix_appointment_for_this_faculty,l1=l1,l2=l2,docname=i[0],facultyid=facultyid)

    else:
        return render_template('loginpage2.html',err='Please enter correct credentials...')
    

## Admin Login Page
@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    username = request.form['username']
    passw = request.form['pass']
    c.execute('SELECT * FROM superusercreds')
    conn.commit()
    superusercreds = c.fetchall()

    for i in superusercreds:
        if str(i[0])==str(username) and str(i[1])==str(passw):
            student_reg_requests = ret_student_reg_requests()
            faculty_reg_requests = ret_faculty_reg_requests()
            registered_student = ret_registered_student()
            registered_faculty = ret_registered_faculty()
            l1 = len(student_reg_requests)
            l2 = len(faculty_reg_requests)
            l3 = len(registered_student)
            l4 = len(registered_faculty)
            return render_template('adminlogin.html',student_reg_requests=student_reg_requests,faculty_reg_requests=faculty_reg_requests,registered_student=registered_student,registered_faculty=registered_faculty,l1=l1,l2=l2,l3=l3,l4=l4)
    else:
        return render_template('loginpage3.html',err='Please enter correct credentials...')
    

## Delete patient from database    
@app.route('/deletestudent',methods=['GET','POST'])
def deletestudent():
    stunum = request.values['stunum']
    c.execute(f"DELETE FROM student WHERE phone_number='{str(stunum)}' ")
    conn.commit()
    student_reg_requests = ret_student_reg_requests()
    faculty_reg_requests = ret_faculty_reg_requests()
    registered_student = ret_registered_student()
    registered_faculty = ret_registered_faculty()
    l1 = len(student_reg_requests)
    l2 = len(faculty_reg_requests)
    l3 = len(registered_student)
    l4 = len(registered_faculty)
    return render_template('adminlogin.html',student_reg_requests=student_reg_requests,faculty_reg_requests=faculty_reg_requests,registered_student=registered_student,registered_faculty=registered_faculty,l1=l1,l2=l2,l3=l3,l4=l4)
    

## Delete doctor from database
@app.route('/deletefaculty',methods=['GET','POST'])
def deletefaculty():
    facultyid = request.values['facultyid']
    c.execute(f"DELETE FROM faculty WHERE faculty_id='{str(facultyid)}' ")
    conn.commit()
    student_reg_requests = ret_student_reg_requests()
    faculty_reg_requests = ret_faculty_reg_requests()
    registered_student = ret_registered_student()
    registered_faculty = ret_registered_faculty()
    l1 = len(student_reg_requests)
    l2 = len(faculty_reg_requests)
    l3 = len(registered_student)
    l4 = len(registered_faculty)
    return render_template('adminlogin.html',student_reg_requests=student_reg_requests,faculty_reg_requests=faculty_reg_requests,registered_student=registered_student,registered_faculty=registered_faculty,l1=l1,l2=l2,l3=l3,l4=l4)
   

## Patient Function to make appointment
@app.route('/makeappointment',methods=['GET','POST'])
def makeappointment():
    stunum = request.args['phn']
    appdate = request.form['appdate']
    whichfaculty = request.form['whichfaculty']
    facname = whichfaculty.split('-')[0]
    facultyid = whichfaculty.split('-')[1]
    stuname = getstuname(stunum)
    appdate2 = datetime.strptime(appdate, '%Y-%m-%d').strftime("%Y-%m-%d")
    print(appdate2,datetoday())
    if appdate2>datetoday():
        if stuname!=-1:
            c.execute(f"INSERT INTO facultyappointmentrequests VALUES ('{facultyid}','{stuname}','{stunum}','{appdate}')")
            conn.commit()
            facultyandapps,l = retallfacultyandapps()
            facname_facultyid,l2 = ret_facname_facdept()
            facnames = []
            for i in facultyandapps:
                facnames.append(getfacname(i[0]))
            return render_template('studentlogin.html',mess=f'Appointment Request sent to Faculty.',facnames=facnames,facultyandapps=facultyandapps,facname_facultyid=facname_facultyid,l=l,l2=l2,stuname=stuname) 
        else:
            facultyandapps,l = retallfacultyandapps()
            facname_facultyid,l2 = ret_facname_facdept()
            facnames = []
            for i in facultyandapps:
                facnames.append(getfacname(i[0]))
            return render_template('studentlogin.html',mess=f'No user with such contact number.',facnames=facnames,facultyandapps=facultyandapps,facname_facultyid=facname_facultyid,l=l,l2=l2,stuname=stuname) 
    else:
        facultyandapps,l = retallfacultyandapps()
        facname_facultyid,l2 = ret_facname_facdept()
        facnames = []
        for i in facultyandapps:
            facnames.append(getfacname(i[0]))
        return render_template('studentlogin.html',mess=f'Please select a date after today.',facnames=facnames,facultyandapps=facultyandapps,facname_facultyid=facname_facultyid,l=l,l2=l2,stuname=stuname) 


## Approve Doctor and add in registered faculty
@app.route('/approvefaculty')
def approvefaculty():
    doctoapprove = request.values['facultyid']
    c.execute('SELECT * FROM faculty')
    conn.commit()
    doctor_requests = c.fetchall()
    for i in doctor_requests:
        if str(i[5])==str(doctoapprove):
            c.execute(f"UPDATE faculty SET status=1 WHERE faculty_id={str(doctoapprove)}")
            conn.commit()
            student_reg_requests = ret_student_reg_requests()
            faculty_reg_requests = ret_faculty_reg_requests()
            registered_student = ret_registered_student()
            registered_faculty = ret_registered_faculty()
            l1 = len(student_reg_requests)
            l2 = len(faculty_reg_requests)
            l3 = len(registered_student)
            l4 = len(registered_faculty)
            return render_template('adminlogin.html',mess=f'Doctor Approved successfully!!!',student_reg_requests=student_reg_requests,faculty_reg_requests=faculty_reg_requests,registered_student=registered_student,registered_faculty=registered_faculty,l1=l1,l2=l2,l3=l3,l4=l4) 
    else:
        student_reg_requests = ret_student_reg_requests()
        faculty_reg_requests = ret_faculty_reg_requests()
        registered_student = ret_registered_student()
        registered_faculty = ret_registered_faculty()
        l1 = len(student_reg_requests)
        l2 = len(faculty_reg_requests)
        l3 = len(registered_student)
        l4 = len(registered_faculty)
        return render_template('adminlogin.html',mess=f'Doctor Not Approved...',student_reg_requests=student_reg_requests,faculty_reg_requests=faculty_reg_requests,registered_student=registered_student,registered_faculty=registered_faculty,l1=l1,l2=l2,l3=l3,l4=l4) 


## Approve Patient and add in registered student
@app.route('/approvestudent')
def approvestudent():
    stutoapprove = request.values['stunum']
    c.execute('SELECT * FROM student')
    conn.commit()
    student_requests = c.fetchall()
    for i in student_requests:
        if str(i[3])==str(stutoapprove):
            c.execute(f"UPDATE student SET status=1 WHERE phone_number={str(stutoapprove)}")
            conn.commit()
            student_reg_requests = ret_student_reg_requests()
            faculty_reg_requests = ret_faculty_reg_requests()
            registered_student = ret_registered_student()
            registered_faculty = ret_registered_faculty()
            l1 = len(student_reg_requests)
            l2 = len(faculty_reg_requests)
            l3 = len(registered_student)
            l4 = len(registered_faculty)
            return render_template('adminlogin.html',mess=f'Student Approved successfully!!!',student_reg_requests=student_reg_requests,faculty_reg_requests=faculty_reg_requests,registered_student=registered_student,registered_faculty=registered_faculty,l1=l1,l2=l2,l3=l3,l4=l4) 

    else:
        student_reg_requests = ret_student_reg_requests()
        faculty_reg_requests = ret_faculty_reg_requests()
        registered_student = ret_registered_student()
        registered_faculty = ret_registered_faculty()
        l1 = len(student_reg_requests)
        l2 = len(faculty_reg_requests)
        l3 = len(registered_student)
        l4 = len(registered_faculty)
        return render_template('adminlogin.html',mess=f'Student Not Approved...',student_reg_requests=student_reg_requests,faculty_reg_requests=faculty_reg_requests,registered_student=registered_student,registered_faculty=registered_faculty,l1=l1,l2=l2,l3=l3,l4=l4) 


## Approve an appointment request
@app.route('/facultyapproveappointment')
def facultyapproveappointment():
    facultyid = request.values['facultyid']
    stunum = request.values['stunum']
    stuname = request.values['stuname']
    appdate = request.values['appdate']
    c.execute(f"INSERT INTO facultyappointments VALUES ('{facultyid}','{stuname}','{stunum}','{appdate}')")
    conn.commit()
    c.execute(f"DELETE FROM facultyappointmentrequests WHERE studentnum='{str(stunum)}'")
    conn.commit()
    appointment_requests_for_this_faculty,l1 = retapprequests(facultyid)
    fix_appointment_for_this_faculty,l2 = retfacultyandapps(facultyid)
    return render_template('facultylogin.html',appointment_requests_for_this_faculty=appointment_requests_for_this_faculty,fix_appointment_for_this_faculty=fix_appointment_for_this_faculty,l1=l1,l2=l2,facultyid=facultyid)


## Delete an appointment request
@app.route('/facultydeleteappointment')
def facultydeleteappointment():
    facultyid = request.values['facultyid']
    stunum = request.values['stunum']
    c.execute(f"DELETE FROM facultyappointmentrequests WHERE studentnum='{str(stunum)}'")
    conn.commit()
    appointment_requests_for_this_faculty,l1 = retapprequests(facultyid)
    fix_appointment_for_this_faculty,l2 = retfacultyandapps(facultyid)
    return render_template('facultylogin.html',appointment_requests_for_this_faculty=appointment_requests_for_this_faculty,fix_appointment_for_this_faculty=fix_appointment_for_this_faculty,l1=l1,l2=l2,facultyid=facultyid)


## Delete a doctor registration request
@app.route('/deletefacultyrequest')
def deletefacultyrequest():
    facultyid = request.values['facultyid']
    c.execute(f"DELETE FROM faculty WHERE faculty_id='{str(facultyid)}'")
    conn.commit()
    student_reg_requests = ret_student_reg_requests()
    faculty_reg_requests = ret_faculty_reg_requests()
    registered_student = ret_registered_student()
    registered_faculty = ret_registered_faculty()
    l1 = len(student_reg_requests)
    l2 = len(faculty_reg_requests)
    l3 = len(registered_student)
    l4 = len(registered_faculty)
    return render_template('adminlogin.html',student_reg_requests=student_reg_requests,faculty_reg_requests=faculty_reg_requests,registered_student=registered_student,registered_faculty=registered_faculty,l1=l1,l2=l2,l3=l3,l4=l4) 


## Delete a patient registration request
@app.route('/deletestudentrequest')
def deletestudentrequest():
    stunum = request.values['stunum']
    c.execute(f"DELETE FROM student WHERE phone_number='{str(stunum)}'")
    conn.commit()
    student_reg_requests = ret_student_reg_requests()
    faculty_reg_requests = ret_faculty_reg_requests()
    registered_student = ret_registered_student()
    registered_faculty = ret_registered_faculty()
    l1 = len(student_reg_requests)
    l2 = len(faculty_reg_requests)
    l3 = len(registered_student)
    l4 = len(registered_faculty)
    return render_template('adminlogin.html',student_reg_requests=student_reg_requests,faculty_reg_requests=faculty_reg_requests,registered_student=registered_student,registered_faculty=registered_faculty,l1=l1,l2=l2,l3=l3,l4=l4) 


@app.route('/updatestudent')
def updatestudent():
    phn = request.args['phn']
    fn,ln,dob,phn,passw,add,status = getstudetails(phn)
    return render_template('updatestudent.html',fn=fn,ln=ln,dob=dob,phn=phn,passw=passw,add=add,status=status) 


@app.route('/updatefaculty')
def updatefaculty():
    facultyid = request.args['facultyid']
    fn,ln,dob,phn,add,facultyid,passw,dept,status = getfacdetails(facultyid)
    return render_template('updatefaculty.html',fn=fn,ln=ln,dob=dob,phn=phn,passw=passw,add=add,status=status,dept=dept,facultyid=facultyid) 

@app.route('/makefacultyupdates',methods=['GET','POST'])
def makefacultyupdates():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    dob = request.form['dob']
    phn = request.form['phn']
    address = request.form['address']
    facultyid = request.args['facultyid']
    dept = request.form['department']
    c.execute("UPDATE faculty SET first_name=(?) WHERE faculty_id=(?)",(firstname,facultyid))
    conn.commit()
    c.execute("UPDATE faculty SET last_name=(?) WHERE faculty_id=(?)",(lastname,facultyid))
    conn.commit()
    c.execute("UPDATE faculty SET dob=(?) WHERE faculty_id=(?)",(dob,facultyid))
    conn.commit()
    c.execute("UPDATE faculty SET phone_number=(?) WHERE faculty_id=(?)",(phn,facultyid))
    conn.commit()
    c.execute("UPDATE faculty SET address=(?) WHERE faculty_id=(?)",(address,facultyid))
    conn.commit()
    c.execute("UPDATE faculty SET department=(?) WHERE faculty_id=(?)",(dept,facultyid))
    conn.commit()
    return render_template('home.html',mess='Updations Done Successfully!!!') 

    
@app.route('/makestudentupdates',methods=['GET','POST'])
def makestudentupdates():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    dob = request.form['dob']
    phn = request.args['phn']
    address = request.form['address']
    c.execute("UPDATE student SET first_name=(?) WHERE phone_number=(?)",(firstname,phn))
    conn.commit()
    c.execute("UPDATE student SET last_name=(?) WHERE phone_number=(?)",(lastname,phn))
    conn.commit()
    c.execute("UPDATE student SET dob=(?) WHERE phone_number=(?)",(dob,phn))
    conn.commit()
    c.execute("UPDATE student SET address=(?) WHERE phone_number=(?)",(address,phn))
    conn.commit()
    return render_template('home.html',mess='Updations Done Successfully!!!') 

### end of scheduling code

### start of todo code


#### Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True, port = 5001)