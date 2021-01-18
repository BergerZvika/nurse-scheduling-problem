import random

import shift_min
import csp
import hill_climbing
import MaxShifts
import genetic
import function as f
import new_starts_hill_climbing
import simulated_annealing
import ml

# const value
num_shifts = 3
num_days = 7
option = 1
# default value
nurses = 30
per_shift = [3, 5, 4, 4, 3, 3, 4, 4, 4, 5, 5, 5, 4, 4, 5, 3, 4, 4, 4, 4, 3, 5, 4, 4, 5, 3, 4, 3, 4, 5]
shift =          ["011 101 000 010 111 010 101",
                  "000 010 010 010 100 111 111",
                  "001 000 000 011 100 001 010",
                  "100 000 010 010 101 001 100",
                  "000 000 010 010 100 010 010",
                  "100 010 001 010 010 000 110",
                  "000 000 010 001 100 001 110",
                  "000 111 010 010 000 010 110",
                  "010 010 010 010 100 000 010",
                  "111 010 010 000 100 111 100",
                  "011 101 000 010 111 010 101",
                  "000 010 010 010 100 111 111",
                  "001 000 000 011 100 001 010",
                  "100 000 010 010 101 001 100",
                  "000 000 010 010 100 010 010",
                  "100 000 001 010 010 000 110",
                  "000 000 010 001 100 001 110",
                  "000 111 010 011 000 010 110",
                  "010 010 010 010 100 000 010",
                  "111 000 010 000 100 111 100",
                  "011 101 000 010 111 010 101",
                  "000 010 010 010 100 111 111",
                  "001 101 000 011 100 001 010",
                  "100 000 010 010 101 001 100",
                  "000 000 010 010 100 010 010",
                  "100 000 001 010 010 000 110",
                  "000 000 010 001 100 001 110",
                  "000 111 010 010 000 010 110",
                  "010 010 010 010 100 000 010",
                  "111 000 010 000 100 111 100",]



def generate_nurse_shifts():  # this function generate a nurse list
    nurse_list = []
    nuers_schedual = ""
    for n in range(nurse):
        nuers_schedual = ""
        for day in range(num_days):
            for hour in range(num_shifts):
                nuers_schedual += str(random.randint(0, 1))  # random a number
            if day != num_days - 1:
                nuers_schedual += " "  # do a backspace
        nurse_list.append(nuers_schedual)  # insert the weekly shift of the nurse

    for n in range(nurse):
        print('Nurse %d wants to work in:' % (n + 1))
        print(nurse_list[n])
        print()

    print()
    print()
    print()
    print()

    return nurse_list


def generate_shift_num():
    shift_l = []
    for index in range(nurse):
        shift_l.append(random.randint(2, 4))

    for n in range(nurse):
        print("nurse " + str(n) + " can work only " + str(shift_l[n]) + " shifts")

    return shift_l


if __name__ == '__main__':

    print("welcome to Scheduling nurse problem")
    print("")

    save_values = False
    shift_requests = []
    num_shift = per_shift
    while option != -1:
        if not save_values:
            print('Choose a number of nurse:')
            print('1 - To define a value')
            print('2 - To a default value')
            print('3 - To a random value')
            print('0 - Quit')
            option = int(input())

            if option == 1:
                print("write number of nurse: ")
                nurse = int(input())
                s = []
                print("insert nurses shifts request.")
                print("the input need to look like:\n000 101 000 011 111 000 010")
                print("3 numbers for each day in week.")
                print("1 - request for don't work in this shift")
                print("0 - request for work in this shift")
                print("")
                for i in range(1, nurse + 1):
                    print("please insert shift to nurse number: " + str(i))
                    shift = input()
                    s.append(shift)
                shift_requests = f.input_requerst(s)
                print('would you like to create random shift percentage?')
                print('1 - no')
                print('2 - yes')
                option = int(input())
                if option == 2:
                    num_shift = generate_shift_num()  # generate a random one
            elif option == 2:
                shift_requests = f.input_requerst(shift)  # create static
                nurse = nurses
            elif option == 0:
                exit(0)
            else:
                shift_requests = f.input_requerst(generate_nurse_shifts())  # create random
                print('would you like to create random shift percentage?')
                print('1 - no')
                print('2 - yes')
                option = int(input())
                if option == 2:
                    num_shift = generate_shift_num()  # generate a random one

        print('Choose a technique for scheduling:')
        print('1 - Maximize shifts')
        print('2 - Constraint Satisfaction')
        print('3 - Constraint Satisfaction with minimize shift request')
        print('4 - Hill Climb')
        print('5 - Simulated Annealing')
        print('6 - Hill Climb with n random start')
        print('7 - Genetic algorithm')
        print('0 - Quit')
        option = int(input())
        # option 1
        if option == 1:
            print("")
            print("Maximize shifts with minimize shift request Result:")
            MaxShifts.main(nurse, shift_requests, num_days, num_shifts, num_shift)
            # f.print_result(solve, shift, shift_requests, nurse, num_days, num_shifts, "", status)
        # option 2
        elif option == 3:
            print("")
            print("Constraint Satisfaction Result:")
            shift_min.main(nurse, shift_requests, num_days, num_shifts, num_shift)

        # option 3
        elif option == 4:
            print("")
            print("Hill Climb Result:")
            hill_climbing.main(nurse, shift_requests, num_days, num_shifts, num_shift)


        elif option == 5:
            print("")
            print("Please insert number of iterations: ")
            n = int(input())
            print("")
            print("Simulated Annealing Result:")
            simulated_annealing.main(nurse, shift_requests, num_days, num_shifts, num_shift, n)

        elif option == 7:
            print("")
            print("Please insert number of generate: ")
            gen = int(input())
            print("")
            print("Genetic algorithm Result:")
            genetic.main(nurse, shift_requests, num_days, num_shifts, num_shift, gen)


        elif option == 6:
            print("")
            print("how much random start would you like to do?")
            n_start = int(input())
            print("")
            print("Hill Climb with %d random start Result:" % n_start)
            new_starts_hill_climbing.main(nurse, shift_requests, num_days, num_shifts, num_shift, n_start)

        elif option == 2:
            print("Constraint Satisfaction Result:")
            csp.main(nurse, shift_requests, num_days, num_shifts, num_shift)

        # option 0
        elif option == 0:
            exit(0)

        else:
            print("Wrong answer. Please, choose a valid option.")

        print("would you like to use same values for shift percentage and nurse input?")
        print('1 - yes')
        print('other number - no')
        option = int(input())
        if option == 1:
            save_values = True
        else:
            save_values = False

        option = 1
