from flask import *
from firebase_admin import credentials, auth
from flask_firebase_admin import FirebaseAdmin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
import pyrebase

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

firebaseConfig = {
    "apiKey": "AIzaSyBYhmD6RLpy6M3sMxp1CGGPG4Q58mdqotc",
    "authDomain": "firestore491test.firebaseapp.com",
    "projectId": "firestore491test",
    "storageBucket": "firestore491test.appspot.com",
    "messagingSenderId": "114757450538",
    "appId": "1:114757450538:web:7a1667f419d17b84e87c53",
    "measurementId": "G-8YB6KP4E2T",
    "databaseURL": ''
}
pb = pyrebase.initialize_app(firebaseConfig)

@app.route('/') # by default, web page starts with the login page
def index():
    return render_template("admin_login.html")

# in login screen, email and password inputs are taken. After that below code checks if the given inputs are valid or not
# by checking from the database
@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    #  # Authenticate the user's email and password
    try:    
        pb.auth().sign_in_with_email_and_password(email,password)
        return redirect("/home")
    except:
        # user authentication failed
        pass
    return render_template("admin_login.html")

@app.route('/logout') # after logout operation, web site redirects to the login screen
@firebase.jwt_required
def logout():
    session.clear()
    return redirect("/admin_login")
    
@app.route('/home',methods=["GET", "POST"])
def home():
    return render_template("home.html")

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
    priority = StringField("Priority:")
    age = StringField("Age:")
    submit = SubmitField("Submit")

class EmployeeForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    surname = StringField("Surname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    reg_date =StringField("Registration Date:")
    branch_name = StringField("Branch Name:")
    submit = SubmitField("Submit")   

class ActiveCustomerForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    surname = StringField("Surname:", validators=[DataRequired()])
    priority = StringField("Priority:", validators=[DataRequired()])
    processType =StringField("Process Type:")
    total_waited_time = StringField("Waited Time:")
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

@app.route('/delete_queue_customer/<Queue>/<customer_id>', methods=["GET", "POST"])
def delete_queue_customer(Queue,customer_id):
    queueref = db.collection('Queue').document(Queue).collection('TicketsInQueue')
    query = queueref.where("customer_id", "==", customer_id).stream()
    for doc in query:
        queueref.document(doc.id).delete()      # deleting the employee who has passed uid when found
    return redirect('/queue/<Queue>')

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
        customer['email'] = request.form['email']
        customer['surname'] = request.form['surname']
        customer['priority'] = request.form['priority']
        customer['age'] = request.form['age']
        try:
            customersref.document(doc.id).update(customer) # Update the customer document in the Customers collection
            flash("User Updated Successfully!")
            return redirect("customer_edit.html", uid=uid)
        except:
            flash("Error! Looks like there was a problem...try again!")
            return render_template("customer_edit.html", form=form, customer=customer, uid=uid)
    else:
        return render_template("customer_edit.html", form=form, customer=customer, uid=uid)#delete ekle

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
        employee['email'] = request.form['email']
        employee['surname'] = request.form['surname']
        employee['reg_date'] = request.form['reg_date']

        branchesref= db.collection('Branches')
        branch_query = branchesref.where("name", "==", request.form['branch_name']).stream()  
        new_branch = {}
        for result in branch_query:
            new_branch = result.to_dict()
        employee['branch']=new_branch
    
        try:
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
        active_customer['name'] = request.form['name']
        active_customer['priority'] = request.form['priority']
        active_customer['surname'] = request.form['surname']
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

@app.route("/add_employee/<name>", methods = ["POST", "GET"])
def add_employee(name):
    form=EmployeeForm()
    employee={}
    if request.method == "POST":#Only listen to POST
        # Update the employee fields with the form data
        employee['name'] = request.form['name']
        employee['email'] = request.form['email']
        employee['surname'] = request.form['surname']
        employee['reg_date'] = request.form['reg_date']
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


if __name__ == "__main__":
    app.run(debug=True)

##### to do #####
#log out kitle -bişe ekledim ama login autha bağlı olmadığından deneyemedim
#css queue cust editte gözükmüyor, düzelt
#formlarda değişmeyecek kısımları kitle
#add employee sign in yapamıyor
#login i autha bağlamayı dene -firebase_admin.auth olmadı password doğrulamıyor, pyrebase i deniyorum ama setup sıkıntı var sanırım
#UI improvements
#dashboarda başla
#total waited time gözükmüyor bi sor
#queue cust editte priorityi sadece o queue için geçici ayarlıyoruz bence ok ama yine de sor
#admin customer eklesin mi?