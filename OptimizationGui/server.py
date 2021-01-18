from flask import Flask, render_template, request, send_file
import shift_min
import hill_climbing
import MaxShifts
import genetic
import function as f
import new_starts_hill_climbing
import simulated_annealing
import DataToSend as dt
import csp
import json
import os

num_days = 7
num_shifts = 3
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("NspGui.html")


@app.route('/get_data', methods=['GET'])
def get_data():
    data = dt.get_list()
    dt.clear()  # clear all the data for future runs
    return render_template('result_output.html', shifts=data)


@app.route('/user_data', methods=['POST'])
def user_input():
    # read json + reply
    data = request.get_json()  # load the data as json
    shifts_requests = f.input_requerst(data[0])  # take the shifts requests
    per_shift = list(map(int, data[1]))  # get the shift percentage
    result = []
    if data[2][0] == "MaxShifts":
        result = MaxShifts.main(len(shifts_requests), shifts_requests, num_days, num_shifts, per_shift)
    elif data[2][0] == "shift_min":
        result = shift_min.main(len(shifts_requests), shifts_requests, num_days, num_shifts, per_shift)
    elif data[2][0] == "csp":
        result = csp.main(len(shifts_requests), shifts_requests, num_days, num_shifts, per_shift)
    elif data[2][0] == "hill_climbing":
        result = hill_climbing.main(len(shifts_requests), shifts_requests, num_days, num_shifts, per_shift)
    elif data[2][0] == "random_restart":
        result = new_starts_hill_climbing.main(len(shifts_requests), shifts_requests, num_days, num_shifts, per_shift,
                                               int(data[2][1]))
    elif data[2][0] == "genetic":
        result = genetic.main(len(shifts_requests), shifts_requests, num_days, num_shifts, per_shift, int(data[2][1]))
    else:
        result = simulated_annealing.main(len(shifts_requests), shifts_requests, num_days, num_shifts, per_shift,
                                          int(data[2][1]))

    return json.dumps(result)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port='80')
