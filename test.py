from flask import *
from firebase_admin import credentials, firestore
from flask_firebase_admin import FirebaseAdmin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField
from wtforms.validators import DataRequired
import os


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
app.secret_key= "secret"


@app.route('/')
def index():
    return render_template("admin_login.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    users_ref = db.collection('Employees')
    query = users_ref.where('email', '==', email).get()

    if len(query) == 1:
        user = query[0]
        if user.to_dict()['password'] == password:
            session["email"]=email  #session mechanism does not work SOLVE !!
            # user authentication succeeded
            return render_template("view_branch.html")
        else:
            # user authentication failed
            pass
    else:
        # user authentication failed
        pass
    return render_template("admin_login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/home')
def home():
    return render_template("home.html")

########### view list parts
@app.route('/branch',methods=["GET", "POST"])
def branch():# this shows all the branches in the db
    branchesref = db.collection('Branches')
    docs = branchesref.stream()
    headings=['name','location']
    data=[]
    for doc in docs:
        temp = []
        for header in headings:
            temp.append(doc.to_dict()[header])
        data.append(temp)

    return render_template("view_branch.html", data=data, headings=headings)

@app.route('/branch_emp/<name>',methods=["GET", "POST"])
def branch_employee(name):# this shows the employees according to which branch they are located in the db
    employeesref = db.collection('Employees')
    headings=['name','surname','reg_date','email','branch','uid']
    data=[]
    query = employeesref.where("branch.name","==", name).stream()
    for doc in query:
        temp = []
        for header in headings:
            if header!='branch':
                temp.append(doc.to_dict()[header])
            else:
                temp.append(doc.to_dict()[header]['name'])
        data.append(temp)
    return render_template("view_branch_emp.html", data=data, headings=headings)

@app.route('/emp',methods=["GET", "POST"])
def employee():# this shows all the employees in the db
    employeesref = db.collection('Employees')
    headings=['name','surname','reg_date','email','branch','uid']
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
    headings=['name','surname','priority','email','age','uid']
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

#not ready
#this will show te queues details and the active customers in the queues
@app.route('/queue',methods=["GET", "POST"])
def queue():
    queuesref = db.collection('Queue')
    docs =queuesref.stream()
    queue_list=[]
    for doc in docs:
        queue_list.append('{} : {}'.format(doc.id,doc.to_dict()))
    return queue_list   

########### manage/update parts

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
    branch_location = StringField("Branch Location:")
    submit = SubmitField("Submit")    

@app.route('/delete_customer/<uid>', methods=["GET", "POST"])
def delete_customer(uid):
    customersref = db.collection('Customers')
    query = customersref.where("uid", "==", uid).stream()
    for doc in query:
        customersref.document(doc.id).delete()    
    return redirect('http://127.0.0.1:5000/cust')

@app.route('/delete_employee/<uid>', methods=["GET", "POST"])
def delete_employee(uid):
    employeesref = db.collection('Employees')
    query = employeesref.where("uid", "==", uid).stream()
    for doc in query:
        employeesref.document(doc.id).delete()        
    return redirect('http://127.0.0.1:5000/emp')

@app.route('/customer_edit/<uid>', methods=["GET","POST"])
def customer_edit(uid):
    # Query the Customers collection to get the customer with the specified uid
    customersref = db.collection('Customers')
    form = CustomerForm()
    query = customersref.where("uid", "==", uid).stream()
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
            # Update the customer document in the Customers collection
            customersref.document(doc.id).update(customer)
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
    query = employeesref.where("uid", "==", uid).stream()
    for doc in query:
        employee = doc.to_dict()
    if request.method == "POST":
        # Update the employee fields with the form data
        employee['name'] = request.form['name']
        employee['email'] = request.form['email']
        employee['surname'] = request.form['surname']
        employee['reg_date'] = request.form['reg_date']
        employee['branch']['name'] = request.form['branch_name']
        employee['branch']['location'] = request.form['branch_location']
        try:
            # Update the employee document in the Employees collection
            employeesref.document(doc.id).update(employee)
            flash("User Updated Successfully!")
            return redirect("employee_edit.html", uid=uid)
        except:
            flash("Error! Looks like there was a problem...try again!")
            return render_template("employee_edit.html", form=form, employee=employee, uid=uid)
    else:
        return render_template("employee_edit.html", form=form, employee=employee, uid=uid)#delete ekle

if __name__ == "__main__":
    app.run(debug=True)