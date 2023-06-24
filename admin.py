from flask import *
from config_db import*
from datetime import date
import update_lists
import view_lists
import simulation_web
from datetime import date
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# routes connections
app.add_url_rule('/delete_customer/<uid>',methods=['GET','POST'],view_func=update_lists.delete_customer)
app.add_url_rule('/delete_employee/<uid>',methods=['GET','POST'], view_func=update_lists.delete_employee)
app.add_url_rule('/delete_admin/<uid>',methods=['GET','POST'], view_func=update_lists.delete_admin)
app.add_url_rule('/delete_queue_customer/<Queue>/<customer_id>', methods=['GET','POST'],view_func=update_lists.delete_queue_customer)
app.add_url_rule('/customer_edit/<uid>',methods=['GET','POST'], view_func=update_lists.customer_edit)
app.add_url_rule('/employee_edit/<uid>',methods=['GET','POST'], view_func=update_lists.employee_edit)
app.add_url_rule('/admin_edit/<uid>', methods=['GET','POST'],view_func=update_lists.admin_edit)
app.add_url_rule('/queue_cust_edit/<Queue>/<customer_id>', methods=['GET','POST'],view_func=update_lists.queue_cust_edit)
app.add_url_rule('/add_customer', methods=['GET','POST'],view_func=update_lists.add_customer)
app.add_url_rule('/add_branch', methods=['GET','POST'],view_func=update_lists.add_branch)
app.add_url_rule('/add_employee/<name>', methods=['GET','POST'],view_func=update_lists.add_employee)
app.add_url_rule('/branch', methods=['GET','POST'],view_func=view_lists.branch)
app.add_url_rule('/branch_emp/<name>', methods=['GET','POST'],view_func=view_lists.branch_employee)
app.add_url_rule('/queue/<Queue>',methods=['GET','POST'], view_func=view_lists.queue)
app.add_url_rule('/emp', methods=['GET','POST'],view_func=view_lists.employee)
app.add_url_rule('/cust', methods=['GET','POST'],view_func=view_lists.customer)
app.add_url_rule('/graph_view', methods=['GET','POST'],view_func=simulation_web.graph_view)
app.add_url_rule('/table_view', methods=['GET','POST'],view_func=simulation_web.table_view)

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
def logout():
    session.clear()
    return redirect("/")
    
@app.route('/home',methods=["GET", "POST"])
def home():
    #num of employee
    '''num_of_emp=0
    empref = db.collection('Employees')
    snapshot = empref.get()
    num_of_emp = len(snapshot)
    
    #num of total customer
    num_of_cust_total=0
    customerref = db.collection('Customers')
    snapshot = customerref.get()
    num_of_cust_total = len(snapshot)

    #ticket number according to transaction type in a day(line)
    transaction_list=[]
    transaction_label=[]

    transactionref = db.collection('Transactions')
    query = transactionref.stream()
    for doc in query:
        t_action=doc.to_dict()
        transaction_label.append(t_action['Name'])

    ticketref = db.collection('Tickets')
    today = date.today()
    for transaction in transaction_label:
        t_count=0
        query = ticketref.where('processType','==',transaction).stream()

        for doc in query:
            ticket=doc.to_dict()
            if ticket['date_time'].date()==today:
                t_count+=1
        transaction_list.append(t_count)

    #ticket num for each branch for graph (bar)
    branch_ticket_list=[]
    branch_ticket_label=[]
    today = date.today()#sil
    branchref = db.collection('Branches')
    query = branchref.stream()
    for doc in query:
        branch=doc.to_dict()
        branch_ticket_label.append(branch['name'])
    ticketref = db.collection('Tickets')
    
    for branch in branch_ticket_label:
        b_count = 0
        query = ticketref.where("branch_name", "==", branch).stream()  # filtering according to the passed branch name 
        for doc in query:
            ticket = doc.to_dict()
            if ticket['date_time'].date() == today:
                b_count += 1
        branch_ticket_list.append(b_count)


    #customer in queue num for each branch for graph(line)
    branch_queue_list=[]
    queue_list=[]
    queueref = db.collection('Queue')
    query = queueref.stream()
    for doc in query:
        queue= str(doc.id)
        queue_list.append(queue)
    for queue in queue_list:
        q_count=0
        queueref = db.collection('Queue').document(queue).collection('TicketsInQueue')
        snapshot = queueref.get()
        q_count= len(snapshot)
        branch_queue_list.append(q_count)
    
    return render_template("home.html",num_of_emp=num_of_emp,num_of_cust_total=num_of_cust_total,
                           transaction_list=transaction_list,transaction_label=transaction_label,
                           branch_ticket_list=branch_ticket_list,branch_ticket_label=branch_ticket_label,
                           branch_queue_list=branch_queue_list)'''

@app.route("/settings", methods = ["POST", "GET"])
def settings():
    uid="UutTdUDo5RMOELRT2cIWmGskN473"
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

@app.route("/dynamic_priority", methods = ["POST", "GET"])
def dynamic_priority():
    dpriority={}
    if request.method == "POST":
        # Update the fields with the form data
        dpriority['threshold'] = int(request.form.get('plabel'))

        try:
            #Append data to the firebase realtime database
            prioritiesref = db.collection('DynamicPriority')
            prioritiesref.document('0qtjOL35L28dr35KWxlG').update(dpriority)
            #Go to settings page
            return redirect(url_for('settings'))
        except:
            #If there is any error, redirect to settings page
            return redirect(url_for('settings'))
        
    return render_template('dynamic_priority.html')    

if __name__ == "__main__":
    app.run(debug=True)
