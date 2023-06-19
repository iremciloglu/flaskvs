from flask import *
import subprocess
from config_db import*

def graph_view():
    subprocess.run(['python', 'bank_simulation.py'])
    with open('simulation_results.txt', 'r') as file:
        output = file.readlines()
    return render_template("graph_view.html", output=output[0], output2=output[1])

def table_view():
    subprocess.run(['python', 'bank_simulation.py'])
    with open('simulation_results.txt', 'r') as file:
        output = file.readlines()
    return render_template("table_view.html", output3=output[2],output4=output[3],output5=output[4], output6=output[5])