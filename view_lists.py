from flask import *
from config_db import*



####### view parts 
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
