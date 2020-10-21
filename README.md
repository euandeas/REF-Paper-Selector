# REF-Paper-Selector

Every 4-5 years, Universities in the UK are assessed. This assessment is largely based on how good their research is (there is a separate assessment for teaching quality). This exercise is called the Research Excellence Framework (https://www.ref.ac.uk/). One of the assessments made during this exercise is based on the quality of papers (peer reviewed publications of the research they do e.g. Dupuy et al., 2017) they have published in academic journals, such as Nature and Science, over the last six years. Papers are given a score from 4 to 0 based on their quality, with a 4 being world-leading to 0 being recognised nationally. 

As part of this assessment each University needs to submit a portfolio of their best papers. They therefore need to select a group of papers to submit based on a set of criteria.

# Selection Criteria
1.	Each author must have at least one paper in the final list.
2.	No author can have more than five papers in the final list.
3.	The final list should have the highest possible total score (sum of scores for the selected papers). There may be multiple combinations that will achieve this. 
4.	Some authors may share a paper with another author(s) in the input list. This paper can only be associated with one author.
5.	Where an author has two or more papers eligible for selection, for example more than two papers with the same score for that author, then the script should take one of the following options:

    a.	Print the paper numbers in the terminal window and request the user make a selection.

    b.	Print the paper numbers in the GUI window and request the user make a selection.

    c.	Select one of the papers but flag the paper in output file with the letter ‘A’ to indicate that there are alternative papers that could replace the paper.
  
6.	The final selection should contain a list of n unique papers.

# Output
The script should print the final selection as a .csv file containing n outputs, with the following columns:

  Author - Unique alpha/numeric identifier for the author. 
  
  Paper - Unique numeric code representing a paper.
  
  Score - fractional score for each paper between 0 and 4, in 0.2 increments.
  
  Comment - optional column to flag papers with possible alternatives if using option c above.
  
# Commands
  -h, --help = show this help message and exit
  
  -i [file], --infile [file] = input file name and location e.g. c:/user/REF/input.csv.
  
  -n N, --N N = number of papers to be selected.
  
  -nm, --nMax = create a list of maximum number of papers.
  
  -r [algorithm], --runmode [algorithm] = selection algorithm to use e.g. leastpotential_euandeas.
  
  -o, --output = save to output.csv saved in the same location as the input file.
  
  -ot [file], --outputTo [file] = save ouput to custom filepath.
  
  -va, --validate = run validate_output.py on the final list to check the validity of the final list.
  
  -val [x], --validateLim [x] = validate with a limit of x papers per author (default = 5).
  
  -ve, --verbose = run validate_output.py with verbose output. Only valid if --validate flag is passed.
  
  -s, --show = show score of produced list (rounded to the nearest 0.2).
  
  -sr, --showRaw = show score of produced list.

# Highest Score Out Of Current Algorithms
171.8

This should be done using the test data in the repositry, along with a cap of 50 papers.<br>
The theoretical max of the test data set without meeting the selection criteria is 180.4.

