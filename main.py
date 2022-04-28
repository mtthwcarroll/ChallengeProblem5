import csv
import os

def splitCSV(path, multiple):
    institutions = {}   # dictionary for keeping track of institutions.
    teams = {}   # dictionary for keeping track of teams.
    institutionIndex = 0   # index for institution id
    teamIndex = 1   # index for team dictionary key
    # if there are multiple csv we name each csv "filename+Institution.csv" and "filename+Teams.csv"
    # otherwise it will just be "Institution.csv" and "Teams.csv"
    if multiple:
        name = path[:-4]
    else:
        name = ""
    # Output directory. Check if it exists, if not make one.
    directory = os.path.join(".", "output")
    if not os.path.exists(directory):
        os.mkdir(directory)

    with open(path, 'r') as file:   # open the file in read mode
        csv_read = csv.reader(file)   # make a csv reader from the file
        for row in csv_read:   # iterate over the csv
            if institutionIndex == 0:   # skip the header line
                institutionIndex += 1
                continue
            if institutions.get(row[0]) is None:   # if we haven't seen this institution before
                institutions[row[0]] = [institutionIndex, row[0], row[2], row[3], row[4]]
                institutionIndex += 1
            # add the team to our team dictionary with the institution id
            teams[teamIndex] = [row[1], row[5], row[6], row[7], institutions[row[0]][0]]
            teamIndex += 1
    # actually write the institutions csv.
    try:
        with open(os.path.join(directory, name + "Institutions.csv"), "x", newline="") as file:
            header = ["Institution ID", "City", "State/Province", "Country"]
            csv_write = csv.writer(file)
            csv_write.writerow(header)
            for row in institutions.values():
                csv_write.writerow(row)
    except FileExistsError:
        print(name + "Institutions.csv already exists. Move or delete file in directory")
    # write the teams csv.
    try:
        with open(os.path.join(directory, name + "Teams.csv"), "x", newline="") as file:
            header = ["Team Number", "Advisor", "Problem", "Ranking", "Institution ID"]
            csv_write = csv.writer(file)
            csv_write.writerow(header)
            for row in teams.values():
                csv_write.writerow(row)
    except FileExistsError:
        print(name + "Teams.csv already exists. Move or delete file in directory")


if __name__ == '__main__':
    # First we check if there are multiple csv to convert
    multipleCSV = False
    csvCount = 0
    for file in os.listdir("."):
        if file.endswith(".csv"):
            csvCount += 1
            if csvCount > 1:
                multipleCSV = True
                break
    # if there are multiple csv, we pass true for the 'multiple' flag
    for file in os.listdir("."):
        if file.endswith(".csv"):
            splitCSV(file, multipleCSV)
