from flask import *
from firebase_admin import auth
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import date, datetime
from config_db import*




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

def delete_customer(uid):
    customersref = db.collection('Customers') # db connection with the "Customers" collection
    query = customersref.where("uid", "==", uid).stream() # filtering according to the passed uid input
    for doc in query:
        customersref.document(doc.id).delete()   # deleting the customer who has passed uid when found
    auth.delete_user(uid)   #deleting from auth    
    return redirect('/cust')

def delete_employee(uid):
    employeesref = db.collection('Employees') # db connection with the "Employees" collection
    query = employeesref.where("uid", "==", uid).stream() # filtering according to the passed uid input
    for doc in query:
        employeesref.document(doc.id).delete()      # deleting the employee who has passed uid when found
    auth.delete_user(uid)   #deleting from auth
    return redirect('/emp')

def delete_admin(uid):
    adminref = db.collection('Admins') # db connection with the "Admins" collection
    query = adminref.where("uid", "==", uid).stream() # filtering according to the passed uid input
    for doc in query:
        adminref.document(doc.id).delete()   # deleting the admin who has passed uid when found
    auth.delete_user(uid)   #deleting from auth    
    return redirect('/')

def delete_queue_customer(Queue,customer_id):
    queueref = db.collection('Queue').document(Queue).collection('TicketsInQueue')
    query = queueref.where("customer_id", "==", customer_id).stream()
    for doc in query:
        queueref.document(doc.id).delete()      # deleting the employee who has passed uid when found
   
    return redirect('/queue/<Queue>')#it shows empty list fix

def customer_edit(uid):
    # Query the Customers collection to get the customer with the specified uid
    customersref = db.collection('Customers')
    form = CustomerForm()
    query = customersref.where("uid", "==", uid).stream() # filtering according to the passed uid input
    for doc in query:
        customer = doc.to_dict()
    if request.method == "POST":
        # Update the customer fields with the form data
        try:
            if request.form['name']!=' ':
                customer['name'] = request.form['name']
            else:   
                flash("Enter a name.")
                
            if request.form['surname']!=' ':
                customer['surname'] = request.form['surname']
            else:   
                flash("Enter a surname.")
                
            if request.form['priority']!=' ':
                customer['priority'] = int(request.form['priority'])
            else:   
                flash("Enter a priority.")
               
            if request.form['reg_date']!=' ':
                customer['reg_date'] = request.form['birth_date']#we keep birth day as a reg_date in db
            else:   
                flash("Enter a birth date.")
                
            if request.form['email']!=' ':
                customer['email'] = request.form['email']
            else:   
                flash("Enter an email.")

        except:
            return render_template("customer_edit.html", form=form, customer=customer, uid=uid)
        

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

def employee_edit(uid):
    # Query the Employees collection to get the employee with the specified uid
    employeesref = db.collection('Employees')
    form = EmployeeForm()
    query = employeesref.where("uid", "==", uid).stream()  # filtering according to the passed uid input
    for doc in query:
        employee = doc.to_dict()
    if request.method == "POST":
        # Update the employee fields with the form data
        try:
            if request.form['name']!=' ':
                employee['name'] = request.form['name']
            else:   
                flash("Enter a name.")
                
            if request.form['surname']!=' ':
                employee['surname'] = request.form['surname']
            else:   
                flash("Enter a surname.")
               
            if request.form['reg_date']!=' ':
                employee['reg_date'] = request.form['birth_date']#we keep birth day as a reg_date in db
            else:   
                flash("Enter a birth date.")
                
            if request.form['email']!=' ':
                employee['email'] = request.form['email']
            else:   
                flash("Enter an email.")

        except:
            return render_template("employee_edit.html", form=form, employee=employee, uid=uid)
        
        #updating the branch
        branchesref= db.collection('Branches')
        branch_query = branchesref.where("name", "==", request.form['branch_name']).stream()  
        new_branch = {}
       
        branch_exists = False
        for result in branch_query:
            branch_exists = True
            new_branch = result.to_dict()

        if not branch_exists:
            flash("Enter correct Branch!")  # Display error message
            return render_template("employee_edit.html", form=form, employee=employee, uid=uid)

        employee['branch'] = new_branch

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

def admin_edit(uid):
    #Query the Admins collection to get the admin with the specified uid
    adminref = db.collection('Admins')
    form = AdminForm()
    query = adminref.where("uid", "==", uid).stream() # filtering according to the passed uid input
    for doc in query:
        admin = doc.to_dict()
    if request.method == "POST":
        # Update the admin fields with the form data
        try:
            if request.form['name']!=' ':
                admin['name'] = request.form['name']
            else:   
                flash("Enter a name.")
                
            if request.form['surname']!=' ':
                admin['surname'] = request.form['surname']
            else:   
                flash("Enter a surname.")
               
            if request.form['reg_date']!=' ':
                admin['b_date'] = request.form['birth_date']#we keep birth day as a reg_date in db
            else:   
                flash("Enter a birth date.")
                
            if request.form['email']!=' ':
                admin['email'] = request.form['email']
            else:   
                flash("Enter an email.")
            
            if request.form['password']!=' ':
                admin['password'] = request.form['password']
            else:   
                flash("Enter a password.")

        except:
            return render_template("admin_edit.html", form=form, admin=admin, uid=uid)

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

def queue_cust_edit(Queue,customer_id):
    queueref = db.collection('Queue').document(Queue).collection('TicketsInQueue')
    query = queueref.where("customer_id", "==", customer_id).stream()
    form = ActiveCustomerForm()
    active_customer={}
    for doc in query:
        active_customer = doc.to_dict()

    if request.method == "POST":
        # Update the customer fields with the form data
        try:
            
                
            if request.form['priority']!=' ':
                active_customer['priority'] = int(request.form['priority'])
            else:   
                flash("Enter a priority.")
               
            if request.form['processType']!=' ':
                active_customer['processType'] = request.form['processType']
            else:   
                flash("Enter a process type.")
                
            if request.form['total_waited_time']!=' ':
                active_customer['total_waited_time'] = request.form['total_waited_time']
            else:   
                flash("Enter a waited time.")

        except:
            return render_template("queue_cust_edit.html", form=form, active_customer=active_customer, Queue=Queue, customer_id=customer_id)

        try:
            queueref.document(doc.id).update(active_customer) # Update the customer document in the Queue collection
            flash("User Updated Successfully!")
            return redirect("queue_cust_edit.html", Queue=Queue, customer_id=customer_id)
        except:
            flash("Error! Looks like there was a problem...try again!")
            return render_template("queue_cust_edit.html", form=form, active_customer=active_customer, Queue=Queue, customer_id=customer_id)
    else:
        return render_template("queue_cust_edit.html", form=form, active_customer=active_customer, Queue=Queue, customer_id=customer_id)    

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
    