from ortools.linear_solver import pywraplp
import DataToSend as dt

def main(num_nurses, shift_requests, num_days, num_shifts, max_shift):
    all_nurses = range(num_nurses)
    all_days = range(num_days)
    all_shifts = range(num_shifts)

    solver = pywraplp.Solver.CreateSolver('SCIP')
    nurse_list = shift_requests
    prob_list = []
    # make an input for the problem
    for k in all_nurses:
        line = []
        for i in all_days:
            column = []
            for j in all_shifts:
                column.append(solver.IntVar(0, 1, ''))
            line.append(column)
        prob_list.append(line)

    # any nurse can do only one shift a day
    for nurse in all_nurses:
        for i in all_days:
            solver.Add(solver.Sum([prob_list[nurse][i][j] for j in all_shifts]) <= 1)

    # each shift has to have at least 2 nurses
    for days in all_days:
        for hour in all_shifts:
            solver.Add(
                solver.Sum([prob_list[nurse][days][hour] for nurse in all_nurses]) >= 2)

    # each shift has to have at most 6 nurses
    for days in all_days:
        for hour in all_shifts:
            solver.Add(
                solver.Sum([prob_list[nurse][days][hour] for nurse in all_nurses]) <= 6)

    # insert the nurse constraints
    for nurse in all_nurses:
        # Each nurse works at most num of shifts she can do
        solver.Add(solver.Sum(prob_list[nurse][d][s] for d in all_days for s in all_shifts) <= max_shift[nurse])
        for day in all_days:
            for shift in all_shifts:
                if nurse_list[nurse][day][shift] == 1:  # if the nurse cant take the shift
                    solver.Add(prob_list[nurse][day][shift] == 0)  # make it a constraint

    # Each nurse don't works two shifts in consecutive
    for n in all_nurses:
        for d in all_days:
            next = d + 1
            if next <= num_days - 1:
                solver.Add(prob_list[n][d][2] + prob_list[n][next][0] <= 1)

    # now define the objective
    objective = []
    for nurse in all_nurses:
        nurse_shift = 0
        for days in all_days:
            for hour in all_shifts:
                nurse_shift += prob_list[nurse][days][hour]  # sum all the shifts the nurse take
        objective.append(nurse_shift)

    # we want to maximize the sum of shifts of the nurses
    solver.Maximize(solver.Sum(objective))

    # Solve
    status = solver.Solve()
    # return solver, prob_list, status

    result = []
    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        for d in all_days:
            print('Day', d + 1)
            result.append("Day " + str(d + 1))
            for n in all_nurses:
                for s in all_shifts:
                    if prob_list[n][d][s].solution_value() > 0.5:
                        if shift_requests[n][d][s] == 1:
                            print('Nurse ' + str(n) + ' works shift ' + str(s) + ' (not requested)')
                            result.append('Nurse ' + str(n) + ' works shift ' + str(s) + ' (not requested)')
                        else:
                            print('Nurse ' + str(n) + ' works shift ' + str(s))
                            result.append('Nurse ' + str(n) + ' works shift ' + str(s))
            print("")
        print(
            'Total shifts = ' + str(solver.Objective().Value()) + " / " + str(sum(max_shift)) + " succeed to maximize")
        dt.insert_data('Total shifts = ' + str(solver.Objective().Value()) + " / " + str(sum(max_shift)) + " succeed to maximize")
        print("")
    else:
        print("there is no solution!")
        result.append("there is no solution!")
        dt.insert_data("there is no solution!")

    return result  # return the result
