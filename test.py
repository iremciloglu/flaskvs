from flask import *
from firebase_admin import credentials, auth
from flask_firebase_admin import FirebaseAdmin
from flask_wtf import FlaskForm
from flask_login import login_required, LoginManager,login_user,logout_user
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
import base64
import bcrypt
from datetime import date, datetime, timedelta
import random
import subprocess
import calendar


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
cert = {
        "type": "service_account",
        "project_id": "firestore491test",
        "private_key_id": "5e88bfeaa543c68726e84cd605cafc1b739a238e",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxzQxnf6ARarYE\nTnTMUB5ZE0Lf19/qOe9ygj5LC7enZzgMw9+YrQP6O7i/sEcIsjC/RDN8hYblSUTO\n0yHdorat226HgA5UNw8GRQ6JnM+7UVyTSIQrtYp0Ci3ITTeStAgg1iSLk9xjtijI\nlPQNBELESaO1SUMYtG/XikyYhwgEX0WIkq4ZemWEHLgk2fxvUAWxsREQjCtrTqJw\nMr4CqcO2tWs5nf2aYHz+SpHkxIjF5/0TyLlxCrmZUQQDpJDjCuP1mGe+1RSy+vgn\nJa4b0Wjd3HntWqiqnPwMpEtzvPjJ426MebpVO/GBZwxIL2Y4sb51khMjKU+vghce\n5MZ4JH/1AgMBAAECggEACzxfe8zjYyZgsT36AI1RlaRzdezQ8B7QJGbZo+luJiyO\nLLRWFXJdjXsnriloG8MS9ItNS6GuiB/MsttByR1GuQ7kWbi8bxL5ppZHmGep8vbt\nyDrta0uyH6ojAYTrraAl4VlW/uENrNluk1piX840n+3dZA/opw+D/9V0CLGDzq7R\ngSMzQIoNHFqFQNM23g14DfKapHJWJm45ybPjSenQpNn+od6+CKWRA92nPc4sfbMm\neq5kCpS76iEjOAu4Tqbc1EBlCxQY53Ou8aBTy/AKQFI6glXQ3cPkIqzms9wHzy1h\njo6Igq3butKEpk81xZg5373bO3qHCuePDB5nrWpIkQKBgQDrExjrhKV1MeS6XxEG\nzwHhfcSKc8OzYLa8RjQbKPAaEHOlHTLTvy0dRtLWzr51FMB3CXDY9ube9adaZ7+f\nYIXdZYG+efJAyhqxxE8xd7xEke4YdR/3Vp8OJ/imR503A2xZgAh8cohw2p90iCDV\nl0xKGtPRSRUWtxZJpSf29Jh2SQKBgQDBoMtMeN+Xn/jH0a+ikD5vKBuXVG6OL1lc\ngpffOThwNuwp0wXjZVjqXkK4Hx2UHffS0rA5rO8BAMAcMxfy0NuI27v2ecI46N7j\n/bHGRnIJG3iDXs3Lx3loV2TQjJmsX/9tkbTUmrJdWErTAkxvYw7DYoR2nqkJcKw3\nEprbVNGMTQKBgHZUBZ5ABf1pIQaDZhG0T/EOmslKnn8DttgsynvFbp7gGyZI/VXD\nDNWI2gaQySQsTvlcgjZkijA/HX+Pa9CxCJE6UEXuInhkg21qMKbo65bkkiIziuS4\n8JVyn2Ir+EJB8d9XaG4kRPPxyIQjJcv+PcOrn2Xg0MG/ZXOqs+RGmRwpAoGBAJTJ\nsm75Exe4XbtubcBFhzRzZYBL6QhpagmkcH+fwLa5/Y/GEGhEoKa3+Bz0DA6dWKow\nLCqlsKLcqMMCoAx+YbQw5abouU5x45TehZUO3OISsfCBETLd/XUocteuswe6XNUd\neg9FMHp6NkUfJw0Q2W9abN+Z29rdMfi/2y9fZgahAoGAH36dxNOIJiMMqEdr+YI2\nUD6KacA/0qhFUU63Nx6m7YZ58rkRFLTV1F6qNiZn7QVFgtP4TJlB+m4GruF5V6Y/\nOshSHQ7hU7zmUOsO53aJVe04iLhXdbDTwd2aezBPL7cTHhL4AZ73iFvXlySIaXQl\ni8kF+jnJIddr/H7c7SZ2apw=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-7l56g@firestore491test.iam.gserviceaccount.com",
        "client_id": "112284953008835814355",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-7l56g%40firestore491test.iam.gserviceaccount.com"
        }   
app.config["FIREBASE_ADMIN_CREDENTIAL"] = credentials.Certificate(cert)
firebase = FirebaseAdmin(app)
db = firebase.firestore.client()

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user():
	return db.collection('Admins').document('hMhBXy4cuNT7mG6VRR16').get()

@app.route('/') # by default, web page starts with the login page
def index():
    return render_template("admin_login.html")

# in login screen, email and password inputs are taken. After that below code checks if the given inputs are valid or not
# by checking from the database
@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    users_ref = db.collection('Admins')
    query = users_ref.where('email', '==', email).get()

    if len(query) == 1:
        #In this code block, the variable user is being set to the first result in the query list returned by the where method
        # applied to the users_ref collection, which is filtered by the email entered in the login form.
        user = query[0]
        #Since query is a collection of Firestore documents returned from the get() method,
        # it is a list-like object, so query[0] retrieves the first (and in this case, only) document that matches the specified email.
        if user.to_dict()['password'] == password:
            session["email"]=email
            # user authentication succeeded
            return redirect(url_for("home"))
        else:
            # user authentication failed
            pass
    else:
        # user authentication failed
        pass
    return render_template("admin_login.html")

@app.route('/logout') # after logout operation, web site redirects to the login screen
#@login_required
def logout():
    session.clear()
    return redirect("/")
    
@app.route('/home',methods=["GET", "POST"])
def home():
    #Get the current UTC datetime
    now_utc = datetime.utcnow()
    # Convert to the desired timezone (UTC+2 in this case)
    now = now_utc + timedelta(hours=2)

    num_of_cust_day=0
    ticketsref = db.collection('Tickets') #our database's connection
    docs = ticketsref.stream()
    #for doc in docs.where('date_time','>=',now.day):#idk
       #num_of_cust_day=+1


    #num_of_cust_day=20
    num_of_cust_reg=30#for a month
    num_of_emp=10
    weekly_list=[]
    week_label=['1st week','2nd week','3rd week','4th week']

    week1_ticket=0#ticket num for each week for graph in a month(line)

    #x = np.array(calendar.monthcalendar(now.year, now.month))
   # week_of_month = np.where(x==day)[0][0] + 1

    #for doc in docs.where('date_time','>=',now.month):#fix
        #if doc.where('date_time','>=',now.day-7):
            #week1_ticket=+1
    week2_ticket=173
    week3_ticket=84
    week4_ticket=66
    weekly_list.append(week1_ticket)
    weekly_list.append(week2_ticket)
    weekly_list.append(week3_ticket)
    weekly_list.append(week4_ticket)
    branch_ticket_list=[]
    branch_ticket_label=['Nicosia Branch','Kalkanlı Branch','Kyrenia Branch']
    branch_1_ticket=20#ticket num for each branch for graph in a day(area)
    branch_2_ticket=10
    branch_3_ticket=35
    branch_ticket_list.append(branch_1_ticket)
    branch_ticket_list.append(branch_2_ticket)
    branch_ticket_list.append(branch_3_ticket)
    branch_queue_list=[]
    branch_1_queue=34#customer in queue num for each branch for graph in a day(column)
    branch_2_queue=25
    branch_3_queue=38
    branch_queue_list.append(branch_1_queue)
    branch_queue_list.append(branch_2_queue)
    branch_queue_list.append(branch_3_queue)

    return render_template("home.html",num_of_cust_day=num_of_cust_day,num_of_cust_reg=num_of_cust_reg,num_of_emp=num_of_emp,
                           weekly_list=weekly_list,week_label=week_label,branch_ticket_list=branch_ticket_list,branch_ticket_label=branch_ticket_label,branch_queue_list=branch_queue_list)

####### view parts 
@app.route('/branch',methods=["GET", "POST"])
def branch():# this shows all the branches in the db
    branchesref = db.collection('Branches') #our database's "Branches" collection's connection is shown here
    docs = branchesref.stream()
    headings=['name','Queue'] # needed parameters
    data=[]
    for doc in docs:
        temp = []
        try:
            for header in headings:
                if header == 'Queue':#we are keeping the queue as a directory in Branches collection, so we split it to get wanted data
                    queue_directory=doc.to_dict()[header].split('/')
                    temp.append(queue_directory[2])
                else:    
                    temp.append(doc.to_dict()[header])
        except KeyError:
                temp.append('')  # handle missing fields by adding empty string        
        data.append(temp)

    return render_template("view_branch.html", data=data, headings=headings)

@app.route('/branch_emp/<name>',methods=["GET", "POST"])
def branch_employee(name):# this shows the employees according to which branch they are located in the db
    employeesref = db.collection('Employees')
    headings=['name','surname','reg_date','email','branch','uid'] # needed parameters
    data=[]
    query = employeesref.where("branch.name","==", name).stream() # since specific branch name is passed to here, we are filtering according to it
    for doc in query:
        temp = []
        for header in headings:
            try:
                if header!='branch':
                    temp.append(doc.to_dict()[header])
                else:
                    temp.append(doc.to_dict()[header]['name'])
            except KeyError:
                temp.append('')  # handle missing fields by adding empty string
        data.append(temp)
    return render_template("view_branch_emp.html", data=data, headings=headings)

@app.route('/emp',methods=["GET", "POST"])
def employee():# this shows all the employees in the db
    employeesref = db.collection('Employees')
    headings=['name','surname','reg_date','email','branch','uid'] # needed parameters
    data=[]
    docs = employeesref.stream()
    for doc in docs:
        temp = []
        for header in headings:
            try:
                if header!='branch':
                    temp.append(doc.to_dict()[header])
                else:
                    temp.append(doc.to_dict()[header]['name'])
            except KeyError:
                temp.append('')  # handle missing fields by adding empty string
        data.append(temp)
    return render_template("view_emp.html", data=data, headings=headings)

@app.route('/cust',methods=["GET", "POST"])
def customer():# this shows all the customers in the db
    customersref = db.collection('Customers')
    headings=['name','surname','priority','email','age','uid'] # needed parameters
    data=[]
    docs = customersref.stream()
    for doc in docs:
        temp = []
        for header in headings:
            try:
                temp.append(doc.to_dict()[header])
            except KeyError:
                temp.append('')  # handle missing fields by adding empty string
        data.append(temp)
    return render_template("view_customer.html", data=data, headings=headings)

#this will show the queues details and the active customers in the queues
@app.route('/queue/<Queue>',methods=["GET", "POST"])
def queue(Queue):#it should show position !!
    queueref = db.collection('Queue').document(Queue).collection('TicketsInQueue')
    chosen_queue = queueref.stream()
    headings=['name','surname','priority','processType','total_waited_time','customer_id'] # needed parameters
    data=[]
    for ticket in chosen_queue:
        temp = []
        for header in headings:
            try:
                temp.append(ticket.to_dict()[header])
            except KeyError:
                temp.append('')  # handle missing fields by adding empty string
        data.append(temp)
    return render_template("view_queue.html", data=data, headings=headings, Queue=Queue)  

########### manage/update parts

#these classes make use of flaskform by allowing us to edit wanted fields
class CustomerForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    surname = StringField("Surname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    priority = StringField("Priority:", validators=[DataRequired()])
    birth_date = StringField("Birth date:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class EmployeeForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    surname = StringField("Surname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    birth_date =StringField("Birth Date:", validators=[DataRequired()])
    branch_name = StringField("Branch Name:", validators=[DataRequired()])
    submit = SubmitField("Submit")   

class ActiveCustomerForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    surname = StringField("Surname:", validators=[DataRequired()])
    priority = StringField("Priority:", validators=[DataRequired()])
    processType =StringField("Process Type:")
    total_waited_time = StringField("Waited Time:")
    submit = SubmitField("Submit")  

class AdminForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    surname = StringField("Surname:", validators=[DataRequired()])
    birth_date = StringField("Birth date:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    password = StringField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/delete_customer/<uid>', methods=["GET", "POST"])
def delete_customer(uid):
    customersref = db.collection('Customers') # db connection with the "Customers" collection
    query = customersref.where("uid", "==", uid).stream() # filtering according to the passed uid input
    for doc in query:
        customersref.document(doc.id).delete()   # deleting the customer who has passed uid when found
    auth.delete_user(uid)   #deleting from auth    
    return redirect('/cust')

@app.route('/delete_employee/<uid>', methods=["GET", "POST"])
def delete_employee(uid):
    employeesref = db.collection('Employees') # db connection with the "Employees" collection
    query = employeesref.where("uid", "==", uid).stream() # filtering according to the passed uid input
    for doc in query:
        employeesref.document(doc.id).delete()      # deleting the employee who has passed uid when found
    auth.delete_user(uid)   #deleting from auth
    return redirect('/emp')
@app.route('/delete_admin/<uid>', methods=["GET", "POST"])
def delete_admin(uid):
    adminref = db.collection('Admins') # db connection with the "Admins" collection
    query = adminref.where("uid", "==", uid).stream() # filtering according to the passed uid input
    for doc in query:
        adminref.document(doc.id).delete()   # deleting the admin who has passed uid when found
    auth.delete_user(uid)   #deleting from auth    
    return redirect('/')

@app.route('/delete_queue_customer/<Queue>/<customer_id>', methods=["GET", "POST"])
def delete_queue_customer(Queue,customer_id):
    queueref = db.collection('Queue').document(Queue).collection('TicketsInQueue')
    query = queueref.where("customer_id", "==", customer_id).stream()
    for doc in query:
        queueref.document(doc.id).delete()      # deleting the employee who has passed uid when found
   
    return redirect('/queue/<Queue>')#it shows empty list fix

@app.route('/customer_edit/<uid>', methods=["GET","POST"])
def customer_edit(uid):
    # Query the Customers collection to get the customer with the specified uid
    customersref = db.collection('Customers')
    form = CustomerForm()
    query = customersref.where("uid", "==", uid).stream() # filtering according to the passed uid input
    for doc in query:
        customer = doc.to_dict()
    if request.method == "POST":
        # Update the customer fields with the form data
        customer['name'] = request.form['name']
        customer['surname'] = request.form['surname']
        customer['priority'] = int(request.form['priority'])
        customer['reg_date'] = request.form['birth_date']#we keep birth day as a reg_date in db, idk why
        customer['email'] = request.form['email']

        #updating age according to birth_date
        today = date.today()
        reg_date = datetime.strptime(customer['reg_date'], '%d/%m/%Y').date()
        customer['age'] = today.year - reg_date.year - ((today.month, today.day) < (reg_date.month, reg_date.day))

        try:
            auth.update_user(uid,email=customer['email'])#updating email in firebase auth
            customersref.document(doc.id).update(customer) # Update the customer document in the Customers collection
            flash("User Updated Successfully!")
            return redirect("customer_edit.html", uid=uid)
        except:
            flash("Error! Looks like there was a problem...try again!")
            return render_template("customer_edit.html", form=form, customer=customer, uid=uid)
    else:
        return render_template("customer_edit.html", form=form, customer=customer, uid=uid)

@app.route('/employee_edit/<uid>', methods=["GET","POST"])
def employee_edit(uid):
    # Query the Employees collection to get the employee with the specified uid
    employeesref = db.collection('Employees')
    form = EmployeeForm()
    query = employeesref.where("uid", "==", uid).stream()  # filtering according to the passed uid input
    for doc in query:
        employee = doc.to_dict()
    if request.method == "POST":
        # Update the employee fields with the form data
        employee['name'] = request.form['name']
        employee['surname'] = request.form['surname']
        employee['reg_date'] = request.form['birth_date']
        employee['email'] = request.form['email']
        
        #updating the branch
        branchesref= db.collection('Branches')
        branch_query = branchesref.where("name", "==", request.form['branch_name']).stream()  
        new_branch = {}
        for result in branch_query:
            new_branch = result.to_dict()
        employee['branch']=new_branch
    
        try:
            auth.update_user(uid,email=employee['email'])#updating email in auth
            employeesref.document(doc.id).update(employee) # Update the employee document in the Employees collection
            flash("User Updated Successfully!")
            return redirect("employee_edit.html", uid=uid)
        except:
            flash("Error! Looks like there was a problem...try again!")
            return render_template("employee_edit.html", form=form, employee=employee, uid=uid)
    else:
        return render_template("employee_edit.html", form=form, employee=employee, uid=uid)
    
@app.route('/queue_cust_edit/<Queue>/<customer_id>', methods=["GET","POST"])
def queue_cust_edit(Queue,customer_id):
    queueref = db.collection('Queue').document(Queue).collection('TicketsInQueue')
    query = queueref.where("customer_id", "==", customer_id).stream()
    form = ActiveCustomerForm()
    active_customer={}
    for doc in query:
        active_customer = doc.to_dict()

    if request.method == "POST":
        # Update the customer fields with the form data
        active_customer['priority'] = int(request.form['priority'])
        active_customer['processType'] = request.form['processType']
        active_customer['total_waited_time'] = request.form['total_waited_time']

        try:
            queueref.document(doc.id).update(active_customer) # Update the customer document in the Queue collection
            flash("User Updated Successfully!")
            return redirect("queue_cust_edit.html", Queue=Queue, customer_id=customer_id)
        except:
            flash("Error! Looks like there was a problem...try again!")
            return render_template("queue_cust_edit.html", form=form, active_customer=active_customer, Queue=Queue, customer_id=customer_id)
    else:
        return render_template("queue_cust_edit.html", form=form, active_customer=active_customer, Queue=Queue, customer_id=customer_id)    

@app.route("/add_customer", methods = ["POST", "GET"])
def add_customer():
    form=CustomerForm()
    customer={}
    if request.method == "POST":#Only listen to POST
        # Update the customer fields with the form data
        customer['name'] = request.form['name']
        customer['email'] = request.form['email']
        customer['surname'] = request.form['surname']
        customer['reg_date'] = request.form['birth_date']
        customer['priority'] = int(request.form['priority'])
        customer['password'] = '123456'# password? fix

    #calculating age according to birth_date
        today = date.today()
        reg_date = datetime.strptime(customer['reg_date'], '%d/%m/%Y').date()
        customer['age'] = today.year - reg_date.year - ((today.month, today.day) < (reg_date.month, reg_date.day))
        if customer['age']>65 and customer['priority']<2:
                customer['priority']=2
        try:
            #Try creating the user account using the provided data
            auth_cust= auth.create_user(email=customer['email'], password=customer['password'])
            customer['uid']=auth_cust.uid
            #Append data to the firebase realtime database
            newcustomersref = db.collection('Customers')
            newcustomersref.document().set(customer)
            #Go to customer list page
            return redirect(url_for('customer'))
        except:
            #If there is any error, redirect to customer list page
            return redirect(url_for('customer'))

    else:
        return render_template("add_customer.html",form=form)

@app.route("/add_employee/<name>", methods = ["POST", "GET"])
def add_employee(name):
    form=EmployeeForm()
    employee={}
    if request.method == "POST":#Only listen to POST
        # Update the employee fields with the form data
        employee['name'] = request.form['name']
        employee['email'] = request.form['email']
        employee['surname'] = request.form['surname']
        employee['reg_date'] = request.form['birth_date']
        employee['password'] = '123456'# password? fix

        branchesref= db.collection('Branches')
        branch_query = branchesref.where("name", "==", name).stream()  
        new_branch = {}
        for result in branch_query:
            new_branch = result.to_dict()
        employee['branch']=new_branch

        try:
            #Try creating the user account using the provided data
            auth_emp= auth.create_user(email=employee['email'], password=employee['password'])
            employee['uid']=auth_emp.uid
            #Append data to the firebase realtime database
            newemployeesref = db.collection('Employees')
            newemployeesref.document().set(employee)
            #Go to employee list page
            return redirect(url_for('branch_employee'))
        except:
            #If there is any error, redirect to branch list page
            return redirect(url_for('branch'))

    else:
        return render_template("add_employee.html",name=name,form=form)

@app.route("/simulation", methods = ["POST", "GET"])
def simulation():
    return render_template("simulation.html")

@app.route("/settings", methods = ["POST", "GET"])
def settings():
    uid="wV1jnvGJQEagV5XbcJlKpPdFoeI3"
    adminref = db.collection('Admins')
    query = adminref.where("uid", "==", uid).stream() # filtering according to the passed uid input
    for doc in query:
        admin = doc.to_dict()
    
    return render_template("settings.html", uid=uid,admin=admin)

@app.route("/new_priority_add", methods = ["POST", "GET"])
def new_priority_add():
    priority={}
    if request.method == "POST":
        # Update the fields with the form data
        priority['label'] = request.form.get('plabel')
        priority['level'] = int(request.form.get('plevel'))

        try:
            #Append data to the firebase realtime database
            prioritiesref = db.collection('Priorities')
            prioritiesref.document().set(priority)
            #Go to settings page
            return redirect(url_for('settings'))
        except:
            #If there is any error, redirect to settings page
            return redirect(url_for('settings'))
        
    return render_template('new_priority_adding.html')  



# the route for running the simulation
@app.route('/run_simulation', methods=['POST'])
def run_simulation_route():

    output = subprocess.check_output(['python', 'bank_simulation.py'], universal_newlines=True)
    return render_template('main.html', output=output)
    
def delete_all_customers():
    customersref = db.collection('Customers')
    all_customers = customersref.stream()
    for doc in all_customers:
        delete_customer(doc.uid)
@app.route("/admin_edit/<uid>", methods = ["POST", "GET"])
def admin_edit(uid):
    #Query the Admins collection to get the admin with the specified uid
    adminref = db.collection('Admins')
    form = AdminForm()
    query = adminref.where("uid", "==", uid).stream() # filtering according to the passed uid input
    for doc in query:
        admin = doc.to_dict()
    if request.method == "POST":
        # Update the admin fields with the form data
        admin['name'] = request.form['name']
        admin['surname'] = request.form['surname']
        admin['b_date'] = request.form['birth_date']
        admin['email'] = request.form['email']

        if request.form['password']!="********":
            admin['password'] = request.form['password']

        #updating age according to birth_date
        today = date.today()
        reg_date = datetime.strptime(admin['b_date'], '%d/%m/%Y').date()
        admin['age'] = today.year - reg_date.year - ((today.month, today.day) < (reg_date.month, reg_date.day))

        try:
            auth.update_user(uid,email=admin['email'],password=admin['password'])#updating in firebase auth
            adminref.document(doc.id).update(admin) # Update the admin document in the Admins collection
            flash("User Updated Successfully!")
            return redirect("settings.html", uid=uid)
        except:
            flash("Error! Looks like there was a problem...try again!")
            return render_template("admin_edit.html", form=form, admin=admin, uid=uid)
    else:
        return render_template("admin_edit.html", form=form, admin=admin, uid=uid)
    
@app.route('/graph_view', methods=['POST','GET'])
def graph_view():
    subprocess.run(['python', 'bank_simulation.py'])
    with open('simulation_results.txt', 'r') as file:
        output = file.readlines()
    return render_template("graph_view.html", output=output[0], output2=output[1])

if __name__ == "__main__":
    app.run(debug=True)
