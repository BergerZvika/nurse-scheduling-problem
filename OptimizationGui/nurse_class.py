import numpy as np
import DataToSend as dt

class NurseSchedulingProblem:
    """This class encapsulates the Nurse Scheduling problem
    """

    def __init__(self, hardConstraintPenalty, nurse, shift_requests, num_days, num_shifts, num_shift):
        """
        :param hardConstraintPenalty: the penalty factor for a hard-constraint violation
        """
        self.hardConstraintPenalty = hardConstraintPenalty

        # list of nurses:
        self.nurses = []
        for i in range(nurse):
            self.nurses.append(str(i))

        # nurses' respective shift preferences - morning, evening, night:
        #self.shiftPreference = [[1, 0, 0], [1, 1, 0], [0, 0, 1], [0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 1, 1], [1, 1, 1]]

        # min and max number of nurses allowed for each shift - morning, evening, night:
        self.shiftMin = [2, 2, 2]
        self.shiftMax = [6, 6, 6]

        # max shifts per week allowed for each nurse
        self.ShiftsPerWeek = num_shift

        #nurse request 0 -dont want to work
        self.shiftPreference = shift_requests

        # number of weeks we create a schedule for:
        self.weeks = 1

        # useful values:
        self.shiftPerDay = num_shifts
        self.days = num_days
        self.shiftsPerWeek = self.days * self.shiftPerDay

    def __len__(self):
        """
        :return: the number of shifts in the schedule
        """
        return len(self.nurses) * self.shiftsPerWeek * self.weeks


    def getCost(self, schedule):
        """
        Calculates the total cost of the various violations in the given schedule
        ...
        :param schedule: a list of binary values describing the given schedule
        :return: the calculated cost
        """

        if len(schedule) != self.__len__():
            raise ValueError("size of schedule list should be equal to ", self.__len__())

        # convert entire schedule into a dictionary with a separate schedule for each nurse:
        nurseShiftsDict = self.getNurseShifts(schedule)

        # count the various violations:
        consecutiveShiftViolations = self.countConsecutiveShiftViolations(nurseShiftsDict)
        shiftsPerWeekViolations = self.countShiftsPerWeekViolations(nurseShiftsDict)[1]
        nursesPerShiftViolations = self.countNursesPerShiftViolations(nurseShiftsDict)[1]
        shiftPreferenceViolations = self.countShiftPreferenceViolations(nurseShiftsDict)

        # calculate the cost of the violations:
        hardContstraintViolations = consecutiveShiftViolations + nursesPerShiftViolations + shiftsPerWeekViolations
        softContstraintViolations = shiftPreferenceViolations

        return self.hardConstraintPenalty * hardContstraintViolations + softContstraintViolations

    def getNurseShifts(self, schedule):
        """
        Converts the entire schedule into a dictionary with a separate schedule for each nurse
        :param schedule: a list of binary values describing the given schedule
        :return: a dictionary with each nurse as a key and the corresponding shifts as the value
        """
        shiftsPerNurse = self.__len__() // len(self.nurses)
        nurseShiftsDict = {}
        shiftIndex = 0

        for nurse in self.nurses:
            nurseShiftsDict[nurse] = schedule[shiftIndex:shiftIndex + shiftsPerNurse]
            shiftIndex += shiftsPerNurse

        return nurseShiftsDict

    def countConsecutiveShiftViolations(self, nurseShiftsDict):
        """
        Counts the consecutive shift violations in the schedule
        :param nurseShiftsDict: a dictionary with a separate schedule for each nurse
        :return: count of violations found
        """
        violations = 0
        # iterate over the shifts of each nurse:
        for nurseShifts in nurseShiftsDict.values():
            # look for two cosecutive '1's:
            for shift1, shift2 in zip(nurseShifts, nurseShifts[1:]):
                if shift1 == 1 and shift2 == 1:
                    violations += 1
        return violations

    def countShiftsPerWeekViolations(self, nurseShiftsDict):
        """
        Counts the max-shifts-per-week violations in the schedule
        :param nurseShiftsDict: a dictionary with a separate schedule for each nurse
        :return: count of violations found
        """
        violations = 0
        weeklyShiftsList = []
        # iterate over the shifts of each nurse:
        for index, nurseShifts in enumerate(nurseShiftsDict.values()):  # all shifts of a single nurse
            # iterate over the shifts of each weeks:
            for i in range(0, self.weeks * self.shiftsPerWeek, self.shiftsPerWeek):
                # count all the '1's over the week:
                weeklyShifts = sum(nurseShifts[i:i + self.shiftsPerWeek])
                weeklyShiftsList.append(weeklyShifts)
                if weeklyShifts > self.ShiftsPerWeek[index]:
                    violations += weeklyShifts - self.ShiftsPerWeek[index]
                else:
                    violations += self.ShiftsPerWeek[index] - weeklyShifts


        return weeklyShiftsList, violations

    def countNursesPerShiftViolations(self, nurseShiftsDict):
        """
        Counts the number-of-nurses-per-shift violations in the schedule
        :param nurseShiftsDict: a dictionary with a separate schedule for each nurse
        :return: count of violations found
        """
        # sum the shifts over all nurses:
        totalPerShiftList = [sum(shift) for shift in zip(*nurseShiftsDict.values())]

        violations = 0
        # iterate over all shifts and count violations:
        for shiftIndex, numOfNurses in enumerate(totalPerShiftList):
            dailyShiftIndex = shiftIndex % self.shiftPerDay  # -> 0, 1, or 2 for the 3 shifts per day
            if (numOfNurses > self.shiftMax[dailyShiftIndex]):
                violations += numOfNurses - self.shiftMax[dailyShiftIndex]
            elif (numOfNurses < self.shiftMin[dailyShiftIndex]):
                violations += self.shiftMin[dailyShiftIndex] - numOfNurses

        return totalPerShiftList, violations

    def countShiftPreferenceViolations(self, nurseShiftsDict):
        """
        Counts the nurse-preferences violations in the schedule
        :param nurseShiftsDict: a dictionary with a separate schedule for each nurse
        :return: count of violations found
        """
        violations = 0
        for nurseIndex, shiftPreference in enumerate(self.shiftPreference):
            # duplicate the shift-preference over the days of the period
#            # iterate over the shifts and compare to preferences:
            temp = []
            for i in range(len(shiftPreference)):
                for j in range(len(shiftPreference[i])):
                    temp.append(shiftPreference[i][j])
            shifts = nurseShiftsDict[self.nurses[nurseIndex]]
            for pref, shift in zip(temp, shifts):
                if pref == 1 and shift == 1:
                    violations += 1

        return violations

    def printScheduleInfo(self, schedule):
        """
        Prints the schedule and violations details
        :param schedule: a list of binary values describing the given schedule
        """
        nurseShiftsDict = self.getNurseShifts(schedule)

        print("Schedule for the week:")
        result = []
        for d in range(self.days):
            print('Day', d + 1)
            result.append("Day " + str(d + 1))
            for n in self.nurses:
                for s in range(self.shiftPerDay):
                    if (nurseShiftsDict[n])[(d * self.shiftPerDay) + s] == 1:
                        if self.shiftPreference[int(n)][d][s] == 1:
                            print('Nurse', n, 'works shift', s, '(not requested).')
                            result.append('Nurse ' + str(n) + ' works shift ' + str(s) + ' (not requested)')
                        else:
                            print('Nurse', n, 'works shift', s)
                            result.append('Nurse ' + str(n) + ' works shift ' + str(s))
            print("")

        print("")
        print("Statistics:")
        dt.insert_data("Statistics:")
        print("consecutive shift violations = ", self.countConsecutiveShiftViolations(nurseShiftsDict))
        dt.insert_data("consecutive shift violations = " + str(self.countConsecutiveShiftViolations(nurseShiftsDict)))
        print()

        weeklyShiftsList, violations = self.countShiftsPerWeekViolations(nurseShiftsDict)
        print("number of Shifts for each nurse = ", weeklyShiftsList)
        dt.insert_data("number of Shifts for each nurse = " + str(weeklyShiftsList))
        print("Shifts Per Week Violations = ", violations)
        dt.insert_data("Shifts Per Week Violations = " + str(violations))
        print()

        totalPerShiftList, violations = self.countNursesPerShiftViolations(nurseShiftsDict)
        print("number of Nurses Per Shift = ", totalPerShiftList)
        dt.insert_data("number of Nurses Per Shift = " + str(totalPerShiftList))
        print("Nurses Per Shift Violations = ", violations)
        dt.insert_data("Nurses Per Shift Violations = " + str(violations))
        print()

        shiftPreferenceViolations = self.countShiftPreferenceViolations(nurseShiftsDict)
        print("num of conflict in nurses requests: ", shiftPreferenceViolations)
        dt.insert_data("num of conflict in nurses requests: " + str(shiftPreferenceViolations))
        print()
        return result

# testing the class:
def main():
    # create a problem instance:
    nurses = NurseSchedulingProblem(10)

    randomSolution = np.random.randint(2, size=len(nurses))
    print("Random Solution = ")
    print(randomSolution)
    print()

    nurses.printScheduleInfo(randomSolution)

    print("Total Cost = ", nurses.getCost(randomSolution))


if __name__ == "__main__":
    main()