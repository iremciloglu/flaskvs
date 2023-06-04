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
    