# Algorithm Details
leastpotential_euandeas
-------------
Highest Score: 171.8

This algorithm orders the papers by their score from high to low, and then works through that list from top to bottom and submits valid papers. If the paper has more than one author then it will select the author with the lowest top 5 paper total in order to save the authors with more high scorers for other papers. It will then check if each author has atleast one paper and if not it will try and get their highest scoring paper into the list.

nottingham_lembn
-------------
Highest Score: 171.8

This algorithm sorts all papers in descending order by score. Using this list, papers are added to final list by traversing (in order) though the list of papers. Each author is assigned a value, which represents the total amount of they could potentially add to the final score at any given time. If there are multiple authors for one paper, the author with the lowest score is submitted, saving the more 'valueable' authors for later, so they can submit their higher scoring papers later on. After this traversal, a list of all authors with more than one submitted paper is created, ordered by the score of their lowest scoring paper (ascending). Authors in this list will have their lowest scoring paper replaced by the highest scoring paper of authors who have no submissions.

abased_lembn
-------------
Highest Score: 170.0

This algorithm creates the final list by considering authors instead of looking at papers. The algorithm creates a list of authors, sorted by the score of their highest scoring paper (descending). The list is then traversed (in order) and as each author is passed over, their highest scoring list is submitted to the final list. If there are multiple papers to be considered in a pass (for example if one author has two papers wich both hold the high score), the user is prompted to choose which paper to submit. Because of this user input, there is a range of scores which can be produced for any given dataset using this algorithm, since submitting a paper with multiple authors will leave the co-writers of the paper with more available slots to submit with later on. At the end of the traversal, the author list is re-sorted, to ensure that the authors with the highest scoring papers are at the top. This is because the algorithm will repeat this traversal process until all the slots have been filled, so if the slots get filled halfway through the traversal, the score will be higher if the first half were the higher scoring half of authors.

# Format
Algorithm Name
-------------
Highest Score: 0

Algorithm details
