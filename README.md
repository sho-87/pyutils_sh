# pyutils_sh
Assortment of Python utilities for my personal projects

## Requirements
 - All code tested with Python 3.6 on Windows.
 - Minor adjustments may need to be made for Python 2.7 or other operating systems, but should mostly be OK.
 - Quickest way to get a working Python installation with all the useful dependencies is to install [Anaconda](https://www.continuum.io/downloads)

## crossCorrelation.py
 - This function takes 2 lists/arrays of data and calculates the normalized max cross-correlation value with its associated lag.
 - Additionally, it will also return the cross-correlation value at 0 lag, as well as the entire normalized array as a python list.
 - You can manually set the time constraints by changing the variable values.
 - Requires the numpy module.

## scantronCompile.py
 - Compiles scantron data and calculates exam grades for each student.
 - Also provides a summary of exam performance, as well as a list of the questions "most" students got incorrect and saves the distribution of answers for those poorly performing questions
 - Takes 1 scantron text file and outputs 2 summary grade files.
 - Splitting of the scantron file is specific to each scantron machine. The indices used in this script are correct for the scantron machine in the UBC Psychology department. Indices need to be adjusted for different machines.
 - Scantron exams can be finicky. Students who incorrectly fill out scantrons need to be considered. Make sure to manually inspect the text file output by the scantron machine for missing answers etc. before running this. This script does not correct for human error when filling out the scantron.
 - Requires the pandas module
