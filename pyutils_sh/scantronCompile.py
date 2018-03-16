"""
 - Compiles scantron data and calculates exam grades for each student.
 - Also provides a summary of exam performance, as well as a list of the questions "most" students got incorrect and saves the distribution of answers for those poorly performing questions
 - Takes 1 scantron text file and outputs 2 summary grade files.
 - Splitting of the scantron file is specific to each scantron machine. The indices used in this script are correct for the scantron machine in the UBC Psychology department. Indices need to be adjusted for different machines.
 - Scantron exams can be finicky. Students who incorrectly fill out scantrons need to be considered. Make sure to manually inspect the text file output by the scantron machine for missing answers etc. before running this. This script does not correct for human error when filling out the scantron.
 - Requires the pandas module.

 - Simon Ho (www.simonho.ca)
"""

import csv
import pandas as pd

### BEGIN: options. Fill out these variables for each new exam ###

# text file generated from scantron machine (make sure to manually inspect
# the scantron file first to make sure there are no missing answers etc.)
inputFile = "D:\\scantron.TXT"

# output file from this script. Will contain grades/percentages/answers for all
# students found in the input file
outputGradesFile = "D:\\output_grades.xls"

# an output summary file that will contain overall exam information for
# the class (mean, SD, range, etc.)
outputSummaryFile = "D:\\output_summary.txt"

# list of question numbers to be dropped from all calculations e.g. [1, 3, 5]
dropItems = []

# how many points is each MC question worth?
itemWorth = 1

# Threshold for the summary file. Questions where the correct count is
# less than this proportion/threshold are flagged in the output summary
# file
incorrectThreshold = 0.5

# list containing the CORRECT answers for each question. Update this for
# every exam
correctAnswers = pd.Series([
    "A",  # 1
    "B",  # 2
    "D",  # 3
    "B",  # 4
    "C",  # 5
    "D",  # 6
    "C",  # 7
    "E",  # 8
    "A",  # 9
    "E"  # 10
])

# Start and end locations of various pieces of information in the scantron text file.
# These need to be adjusted for different scantron machine.
# Currently set for the machine used in UBC Psych
surnameIdx = (0, 12)
firstNameIdx = (12, 21)
snumberIdx = (21, 30)
answersIdx = 30

### END: options ###


# calculate total number of points available on the exam
totalExamPoints = (len(correctAnswers)*itemWorth) - len(dropItems)

# open the input scantron file
rawData = csv.reader(open(inputFile, "rb"))

# create a pandas dataframe to hold the scantron data
columns = ["surname", "first name", "student number", "points", "percentage"]
data = pd.DataFrame(columns=columns)

# loop through every row (student) in the input scantron file
for row in rawData:
    # initialize an empty dictionary to hold current student's data
    studentDict = {}
    # get the current student's answers
    answers = row[0][answersIdx:(answersIdx+len(correctAnswers))]
    # store each answer into individual dictionary keys
    for i in range(len(correctAnswers)):
        studentDict[i+1] = answers[i]
    # store student info in dictionary
    studentDict["surname"] = row[0][surnameIdx[0]:surnameIdx[1]]
    studentDict["first name"] = row[0][firstNameIdx[0]:firstNameIdx[1]]
    studentDict["student number"] = row[0][snumberIdx[0]:snumberIdx[1]]

    # calculate points/percentages
    totalPoints = 0
    # loop through every question to check answer
    for j in range(len(correctAnswers)):
        # if the question is to be dropped, don't include it in calculation
        if j+1 in dropItems:
            pass
        # if the answer is correct, add to their running score
        elif correctAnswers[j] == studentDict[j+1]:
            totalPoints += itemWorth
    # store student's total points and exam percentage into dictionary
    studentDict["points"] = totalPoints
    studentDict["percentage"] = float(totalPoints)/totalExamPoints * 100
    # add the dictionary to the dataframe
    data = data.append(studentDict, ignore_index=True)

# save dataframe, with all answers and calculated scores, to output excel file
data.to_excel(outputGradesFile, sheet_name="grades", index=False)

# calculate summary statistics
numStudents = data.shape[0]
meanScore = data["points"].mean()
meanPercentage = data["percentage"].mean()
std = data["points"].std()
scoreRange = (data["points"].min(), data["points"].max())

# calculate problem items and their answer distribution
problemItems = {}

for i in range(len(correctAnswers)):
    if len(data.loc[data[i+1] == correctAnswers[i]]) < (numStudents * incorrectThreshold):
        problemItems[i+1] = {
            "A": len(data.loc[data[i+1] == "A"]),
            "B": len(data.loc[data[i+1] == "B"]),
            "C": len(data.loc[data[i+1] == "C"]),
            "D": len(data.loc[data[i+1] == "D"]),
            "E": len(data.loc[data[i+1] == "E"]),
        }

# create the summary file
summaryFile = open(outputSummaryFile, "wb")

# write descriptive statistics to summary file
lineBreak = "\r\n"

summaryFile.writelines([
    " - Descriptive Statistics -  ", lineBreak*2,
    "N: ", str(numStudents), lineBreak,
    "Mean %: ", str(meanPercentage), "%", lineBreak,
    "Mean score (out of ", str(totalExamPoints), " points): ", str(
        meanScore), lineBreak,
    "Points SD: ", str(std), lineBreak,
    "Range (out of ", str(totalExamPoints), " points): ", str(scoreRange[1] - scoreRange[0]), " (Min: ", str(scoreRange[0]), ", Max: ", str(scoreRange[1]), ")"])

if len(dropItems) != 0:
    summaryFile.writelines([lineBreak, "Dropped questions: "])
    for question in dropItems:
        summaryFile.writelines(["Q", str(question), " "])

# section break
summaryFile.writelines(lineBreak*3)

# write problem items to summary file
summaryFile.writelines([
    " - Problem Items (questions that less than ", str(incorrectThreshold *
        100), "% of students got correct) - ", lineBreak*2
])

if len(problemItems) > 0:
    for question in sorted(problemItems):
        summaryFile.writelines(["Question ", str(question), ": ", lineBreak])
        for answer in sorted(problemItems[question]):
            summaryFile.writelines(
                [str(answer), ": ", str(problemItems[question][answer]), lineBreak])

        summaryFile.writelines(lineBreak)
else:
    summaryFile.writelines("None")

# close the summary file
summaryFile.close()
