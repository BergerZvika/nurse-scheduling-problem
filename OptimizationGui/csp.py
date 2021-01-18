from ortools.constraint_solver.pywrapcp import Solver
from ortools.sat.python import cp_model
import DataToSend as dt

# This program tries to find an optimal assignment of nurses to shifts
# (3 shifts per day, for 7 days), subject to some constraints (see below).
# Each nurse can request to be assigned to specific shifts.
# The optimal assignment maximizes the number of fulfilled shift requests.
def main(num_nurses, shift_requests, num_days, num_shifts, num_shift):
    all_nurses = range(num_nurses)
    all_days = range(num_days)
    all_shifts = range(num_shifts)

    #value of shift for each nurse in week.


    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # Each shift is assigned to at least two nurses in shift.
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_nurses) >= 2)

    # Each shift is assigned to at most four nurses in shift.
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_nurses) <= 6)

    # Each nurse works at most one shift per day.
    for n in all_nurses:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    #Each nurse don't works two shifts in consecutive
    for n in all_nurses:
        for d in all_days:
            next = d + 1
            if next <= num_days - 1:
                model.Add(shifts[(n, d, 2)] + shifts[(n, next, 0)] < 2)

    # Each nurse works at exactly num of shifts he needs
    for n in all_nurses:
            model.Add(sum(shifts[(n, d, s)] for d in all_days for s in all_shifts) == num_shift[n])

    # insert the nurse constraints
    for nurse in all_nurses:
        for day in all_days:
            for shift in all_shifts:
                if shift_requests[nurse][day][shift] == 1:  # if the nurse cant take the shift
                    model.Add(shifts[(nurse, day, shift)] == 0)  # make it a constraint

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # request len
    request_len = 0
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                if shift_requests[n][d][s] == 1:
                    request_len += 1
    result = []
    # print just if there is a solution
    if status != 3:
        for d in all_days:
            print('Day', d + 1)
            result.append("Day " + str(d + 1))
            for n in all_nurses:
                for s in all_shifts:
                    if solver.Value(shifts[(n, d, s)]) == 1:
                        if shift_requests[n][d][s] == 1:
                            print('Nurse', n, 'works shift', s, '(not requested).')
                            result.append('Nurse ' + str(n) + ' works shift ' + str(s) + ' (not requested)')
                        else:
                            print('Nurse', n, 'works shift', s)
                            result.append('Nurse ' + str(n) + ' works shift ' + str(s))
            print("")
            # Statistics.
        print('Statistics')
        dt.insert_data('Statistics')
        print('  - wall time       : %f s' % solver.WallTime())
        dt.insert_data('  - wall time       : %f s' % solver.WallTime())
        print("")
    else:
        print("there is no solution!")
        result.append("there is no solution!")
        dt.insert_data("there is no solution!")
    return result

