#!/usr/bin/python

import os


# TODO : add ability to add and remove from team roster (global pool of 'available' team members to choose from)
# TODO : add ability to add teams to an incentive
# TODO : add ability to add points to specific team member with specific reason for points (upsize, add-a, etc.)

# Key function to sort list by incentive name
def extractName(elem):
    return elem[0]


# Adds a new member to the roster
def addToRoster(name, roster=[]):
    if (name in roster):
        print(name, ' already exists in the roster')
    else:
        roster.append(name)
        roster.sort()
        print('Added ', name, ' to the roster')


# Removes a member from the roster
def removeFromRoster(name, roster=[]):
    if (name in roster):
        roster.remove(name)
        print('Removing ', name, ' from the roster')
    else:
        print(name, ' does not exist in the roster')


# Prints the roster
def printRoster(roster=[]):
    print('            Current Roster:')
    count = 1
    for i in roster:
        print('            ', count, ') ', i[0], ' : ', i[1])
        count += 1


# Prints an Incentive
def printIncentive(incentive=[]):
    print('---------------------------------------------')
    for i in range(len(incentive)):
        if (i == 0):
            print('Name: ' + incentive[i])
        else:
            printTeam(incentive[i])
    print('---------------------------------------------')


# Prints a Team
def printTeam(team=[]):
    print('    ' + team[0] + ':')
    print('        ' + 'Current Points: ' + team[1])
    printRoster(team[2])


# Converts a list with elements of the form '<name>,<points>' to a list of tuples separating the two
def convertRosterToTuples(roster=[]):
    tupledRoster = []
    tuple = []
    print(roster)
    for i in roster:
        print(i)
        tuple.clear()
        tuple = i.split(',')
        tupledRoster.append(tuple.copy())
    printRoster(tupledRoster)
    return tupledRoster.copy()


def convertRosterFromTuples(roster=[]):
    unTupledRoster = []
    raw = ''
    for i in roster:
        raw = i[0] + ',' + i[1]
        unTupledRoster.append(raw)
    return unTupledRoster.copy()


# Parses the incentive file string
def parseIncentives(rawIncentives, incentives=[], names=[]):
    incentive = []
    team = []
    first = True

    SplitOnIncentives = rawIncentives.split('{')

    # For each incentive
    for i in SplitOnIncentives:
        # Removes the first incentive (split creates an empty incentive
        if first:
            first = False
            continue
        SplitOnTeams = i.split(':')
        incentive.clear()
        incentive.append(SplitOnTeams[0])  # Incentive Name
        # For each team
        for j in SplitOnTeams:
            if (j == incentive[0]):
                continue
            else:
                SplitFinal = j.split(';')
                team.clear()
                team.append(SplitFinal[0])  # Team Name
                team.append(SplitFinal[1])  # Team Points
                roster = SplitFinal[2:len(SplitFinal)]  # Team Roster
                roster = convertRosterToTuples(roster)
                team.append(roster.copy())
                incentive.append(team.copy())
        incentives.append(incentive.copy())
        names.append(incentive[0])


# Creates a new incentive
def createIncentive(name, incentives=[], names=[]):
    newIncentive = []
    newIncentive[0] = name
    incentives.append(newIncentive)
    names.append(name)
    names.sort()
    incentives.sort(key=extractName)


# Saves the incentives data
def createIncentiveSaveData(incentive=[]):
    incentiveName = incentive[0]
    saveString = '{' + incentiveName + ':'
    for i in range(len(incentive)):
        if (i == 0):
            continue
        else:
            team = incentive[i]
            teamName = team[0]
            teamPoints = team[1]
            teamRoster = convertRosterFromTuples(team[2])
            saveString = saveString + teamName + ';' + teamPoints + ';'
            for i in teamRoster:
                saveString = saveString + i.rstrip() + ';'
            saveString = saveString[:-1] + ':'
    saveString = saveString[:-1] + '\n'
    return saveString


# Loads a new incentive into the current incentive list
def loadIncentive(name, incentives=[], loadedIncentive=[], teamNames=[]):
    indexOfIncentive = 0

    teamNames.clear()
    loadedIncentive.clear()

    for i in range(len(incentives)):
        if (incentives[i][0] == name):
            indexOfIncentive = i
            break

    print('Loaded \'' + loadedIncentive[0] + '\'...')
    return incentives[indexOfIncentive].copy()


# Loads the data into the proper lists
def loadData(incentives=[], incentiveNames=[], roster=[]):
    # Open roster file if it exists, otherwise creates one
    try:
        fo = open('data/roster.txt', 'r')
        roster = fo.readlines()
        fo.close()
    except FileNotFoundError:
        fo = open('data/roster.txt', 'w+')
        fo.close()

    # Cleans the roster
    for i in range(len(roster)):
        newName = roster[i].rstrip()
        roster[i] = newName

    # Open roster file if it exists, otherwise creates one
    try:
        fo = open('data/incentives.txt', 'r')
        raw = fo.read()
        parseIncentives(raw, incentives, incentiveNames)
        for i in incentives:
            printIncentive(i)
        fo.close()
    except FileNotFoundError:
        fo = open('data/incentives.txt', 'w+')
        fo.close()


# The Main Loop
def main():
    # variable Definition
    roster = []
    incentiveList = []
    incentiveNames = []
    teamNames = []
    command = ''
    selectedIncentive = ''
    currIncentive = []

    loadData(incentiveList, incentiveNames, roster)

    # Automatically selects the first incentive
    if (len(incentiveList) > 0):
        currIncentive = incentiveList[0]
        selectedIncentive = currIncentive[0]
    else:
        selectedIncentive = ""

    # Command Loop
    while command != 'quit':
        if (selectedIncentive != ''):
            print('\nCurrently Selected Incentive: ', selectedIncentive)
        else:
            print('\nNo Incentive Currently Selected')
        command = input('> ')
        if (command == 'add'):
            name = input('Please enter the name of the person you\'d like to add to the roster: ')
            addToRoster(name, roster)
        elif (command == 'show'):
            userSelect = input('Would you like to show \'all\' the incentives? Or the \'current\' One?')
            if (userSelect == 'all'):
                for i in incentiveList:
                    printIncentive(i)
            elif (userSelect == 'current'):
                printIncentive(currIncentive)
            else:
                print('Unrecognized command. Please type either \'all\' or \'current\'.')
        elif (command == 'remove'):
            name = input('Please enter the name of the person you\'d like to remove from the roster: ')
            removeFromRoster(name, roster)
        elif (command == 'new incentive'):
            # Checks if a file with the desired incentive name already exists, if not, creates one
            incentiveName = input('Please enter the name for the new incentive: ')
            createIncentive(incentiveName, incentiveList, incentiveNames)
            # TODO : Fix create incentive
            selectedIncentive = incentiveName
        elif (command == 'select incentive'):
            print('Please choose an incentive from the following: ', end='')
            for i in incentiveNames:
                print(i, end=', ')
            print()
            userSelect = input('    > ')
            if (userSelect in incentiveNames):
                selectedIncentive = userSelect
                currIncentive = (selectedIncentive, incentiveList, currIncentive, teamNames)
            else:
                print('\'', userSelect, '\' does not exist')
        elif (command == 'add team'):
            if (selectedIncentive == ''):
                print('No incentive selected')
            else:
                newTeam = input('Please enter the name for the new team: ')

        elif (command == 'quit'):
            continue
        else:
            print('Command \'', command, '\' not recognized')

    # Save the roster
    fo = open('data/roster.txt', 'w')
    for i in roster:
        fo.write(i + '\n')
    fo.close()

    # Save the incentives
    fo = open('data/incentives.txt', 'w')
    for i in incentiveList:
        raw = createIncentiveSaveData(i)
        fo.write(raw)
    fo.close()


# ----------------------------------------------------------------------------------------------------------------------
if (__name__ == '__main__'):
    # Creates the necessary directories if they don't already exist
    if (os.path.isdir('data') == False):
        os.mkdir('data')
    main()