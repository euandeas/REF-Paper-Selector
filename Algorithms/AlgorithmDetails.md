# Algorithm Details
leastpotential_euandeas
-------------
Highest Score: n/a

This algorithm orders the papers by their score from high to low, and then works through that list from top to bottom and submits valid papers. If the paper has more than one author then it will select the author with the lowest top 5 paper total in order to save the authors with more high scorers for other papers. It will then check if each author has atleast one paper and if not it will try and get their highest scoring paper into the list.

nottingham_lembn
-------------
Highest Score: n/a

This algorithm sorts all papers in descending order by score. Using this list, papers are added to final list by traversing (in order) though the list of papers. Each author is assigned a value, which represents the total amount of they could potentially add to the final score at any given time. If there are multiple authors for one paper, the author with the lowest score is submitted, saving the more 'valueable' authors for later, so they can submit their higher scoring papers later on. After this traversal, a list of all authors with more than one submitted paper is created, ordered by the score of their lowest scoring paper (ascending). Authors in this list will have their lowest scoring paper replaced by the highest scoring paper of authors who have no submissions.

# Format
Algorithm Name
-------------
Highest Score: 0

Algorithm details
