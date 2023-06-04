from flask import *
import subprocess
from config_db import*





#@app.route("/simulation", methods = ["POST", "GET"])
def simulation():
    return render_template("simulation.html")

# the route for running the simulation
#@app.route('/run_simulation', methods=['POST'])
# the route for running the simulation
def run_simulation_route():

    output = subprocess.check_output(['python', 'bank_simulation.py'], universal_newlines=True)
    return render_template('simulation.html', output=output)

def graph_view():
    subprocess.run(['python', 'bank_simulation.py'])
    with open('simulation_results.txt', 'r') as file:
        output = file.readlines()
    return render_template("graph_view.html", output=output[0], output2=output[1])