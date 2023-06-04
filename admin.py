from flask import *
#from flask_login import login_required, LoginManager,login_user,logout_user
from datetime import date, datetime, timedelta
import subprocess
from config_db import*
import update_lists
import view_lists
import simulation_web

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# routes connections
app.add_url_rule('/delete_customer/<uid>',methods=['GET','POST'],view_func=update_lists.delete_customer)
app.add_url_rule('/delete_employee/<uid>',methods=['GET','POST'], view_func=update_lists.delete_employee)
app.add_url_rule('/delete_admin/<uid>',methods=['GET','POST'], view_func=update_lists.delete_admin)
#app.add_url_rule('/delete_all_customer/<uid>', methods=['GET','POST'],view_func=update_lists.delete_all_customers)
app.add_url_rule('/delete_queue_customer/<Queue>/<customer_id>', methods=['GET','POST'],view_func=update_lists.delete_queue_customer)
app.add_url_rule('/customer_edit/<uid>',methods=['GET','POST'], view_func=update_lists.customer_edit)
app.add_url_rule('/employee_edit/<uid>',methods=['GET','POST'], view_func=update_lists.employee_edit)
app.add_url_rule('/admin_edit/<uid>', methods=['GET','POST'],view_func=update_lists.admin_edit)
app.add_url_rule('/queue_cust_edit/<Queue>/<customer_id>', methods=['GET','POST'],view_func=update_lists.queue_cust_edit)
app.add_url_rule('/add_customer', methods=['GET','POST'],view_func=update_lists.add_customer)
app.add_url_rule('/add_employee/<name>', methods=['GET','POST'],view_func=update_lists.add_employee)
app.add_url_rule('/branch', methods=['GET','POST'],view_func=view_lists.branch)
app.add_url_rule('/branch_emp/<name>', methods=['GET','POST'],view_func=view_lists.branch_employee)
app.add_url_rule('/queue/<Queue>',methods=['GET','POST'], view_func=view_lists.queue)
app.add_url_rule('/emp', methods=['GET','POST'],view_func=view_lists.employee)
app.add_url_rule('/cust', methods=['GET','POST'],view_func=view_lists.customer)
app.add_url_rule('/simulation', methods=['GET','POST'],view_func=simulation_web.simulation)
app.add_url_rule('/run_simulation', methods=['GET','POST'],view_func=simulation_web.run_simulation_route)
app.add_url_rule('/graph_view', methods=['GET','POST'],view_func=simulation_web.graph_view)


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
    '''<h2>Lets put some statistics here such as: hold the #customers come that day,#customers register in a month,graph of customer number in week</h2>
  <h2>#employees,graph of #tickets in each branch in a day, how many people in the queue for each branch maybe as a graph?
  </h2>'''
    #Get the current UTC datetime
    now_utc = datetime.utcnow()
    # Convert to the desired timezone (UTC+2 in this case)
    now = now_utc + timedelta(hours=2)

    num_of_cust_day=0
    
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
    week2_ticket=0
    week3_ticket=0
    week4_ticket=0
    weekly_list.append(week1_ticket)
    weekly_list.append(week2_ticket)
    weekly_list.append(week3_ticket)
    weekly_list.append(week4_ticket)
    ######
   
    branch_ticket_list=[]
    branch_ticket_label=['Nicosia Branch','Kalkanlı Branch','Kyrenia Branch']
    branch_1_ticket=0#ticket num for each branch for graph in a day(area)
    branch_2_ticket=0
    branch_3_ticket=0
    #docs= ticketsref.where('date_time','>=',now.day).stream()
   
    
    branch_ticket_list.append(branch_1_ticket)
    branch_ticket_list.append(branch_2_ticket)
    branch_ticket_list.append(branch_3_ticket)
    branch_queue_list=[]
    branch_1_queue=0#customer in queue num for each branch for graph in a day(column)
    branch_2_queue=0
    branch_3_queue=0
    branch_queue_list.append(branch_1_queue)
    branch_queue_list.append(branch_2_queue)
    branch_queue_list.append(branch_3_queue)

    return render_template("home.html",num_of_cust_day=num_of_cust_day,num_of_cust_reg=num_of_cust_reg,num_of_emp=num_of_emp,
                           weekly_list=weekly_list,week_label=week_label,branch_ticket_list=branch_ticket_list,branch_ticket_label=branch_ticket_label,branch_queue_list=branch_queue_list)


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

if __name__ == "__main__":
    app.run(debug=True)
