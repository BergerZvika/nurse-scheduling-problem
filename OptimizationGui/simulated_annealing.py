import os

from nurse_class import NurseSchedulingProblem
import numpy as np
import scipy.constants as constants
import DataToSend as dt
import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


HARD_CONSTRAINT_PENALTY = 10  # the penalty factor for a hard-constraint violation
D = 100


def generate_random_start(nurse_num, num_days, num_shifts):  # this function builds a random start state
    length = nurse_num * num_days * num_shifts  # will tell me the size of the array
    shifts_arr = []
    for i in range(length):
        shifts_arr.append(random.randint(0, 1))
    return shifts_arr


def random_neighbor(current_shifts):  # this function builds all the neighbors of the current state
    length = len(current_shifts) - 1
    rand_index = random.randint(0, length)  # random a index
    temp = current_shifts[0: length + 1]  # make a clone
    if temp[rand_index] == 1:
        temp[rand_index] = 0
    else:
        temp[rand_index] = 1
    return temp


def temperature(t):  # the temperature function
    return pow(0.9, t) * D


def prob_func(T, d_e):  # calculate the probability function
    return np.exp(d_e / T * constants.Boltzmann)


def convert_input(input):  # this function convert the input, 1 is 0 and 0 is 1
    length = len(input)
    temp = input[0:length]
    for i in range(length):
        if temp[i] == 1:
            temp[i] = 0
        else:
            temp[i] = 1
    return temp


# convert the array into vector
def getVec(state, nurse, num_days, num_shifts):
    nurse_shift = []
    for n in range(nurse):
        for day in range(num_days):
            for hour in range(num_shifts):
                nurse_shift.append(state[n][day][hour])
    return nurse_shift


def main(nurse, shift_requests, num_days, num_shifts, num_shift, num_moves):
    nsp = NurseSchedulingProblem(HARD_CONSTRAINT_PENALTY, nurse, shift_requests, num_days, num_shifts,
                                 num_shift)
    current_state = convert_input(getVec(shift_requests, nurse, num_days, num_shifts))
    cost = []
    iteration = []
    current_cost = nsp.getCost(current_state)  # the cost of the current state
    for counter in range(num_moves):
        neighbor = random_neighbor(current_state)  # random a neighbor of the current state
        neighbor_cost = nsp.getCost(neighbor)
        if neighbor_cost < current_cost:
            # if the neighbor cost is better than the cost of the current state
            current_state = neighbor
            current_cost = neighbor_cost
        else:  # the cost of the neighbor is not better than the current state
            T = temperature(counter + 1)  # calculate the temperature
            if T == 0:
                break
            print(counter + 1)
            dt.insert_data(counter + 1)
            counter += 1
            d_E = current_cost - neighbor_cost  # calculate the delta
            prob = prob_func(T, d_E)
            if prob >= np.random.uniform(0, 1):  # update the state with probability
                current_state = neighbor
                current_cost = neighbor_cost
        iteration.insert(len(iteration), counter + 1)
        cost.insert(len(cost), current_cost)
    print("the Minimum local cost is: " + str(nsp.getCost(current_state)))
    dt.insert_data("the Minimum local cost is: " + str(nsp.getCost(current_state)))
    plt.clf()
    plt.ylabel("states cost")
    plt.xlabel("iteration")
    ln, = plt.plot(iteration, cost)
    if os.path.isfile(os.getcwd() + "/static/OptimizationGui.png"):  # first erase the former pic
        os.remove(os.getcwd() + "/static/OptimizationGui.png")
    plt.savefig(os.getcwd() + "/static/OptimizationGui")
    ln.remove()
    # plt.show()
    return nsp.printScheduleInfo(current_state)  # print the current state info
