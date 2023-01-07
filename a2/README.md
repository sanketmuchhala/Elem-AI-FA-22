# samuch-rifhall-akukkapa-a2
Assignment 2 - Fall 2022 - Elements of AI<br />
Sanket Muchhala (samuch), 
Abhiram Kukkapali (akukkapa),
Halloran Riley (rifhall),
<br />

**Part 1 - Raichu**<br />
<br />
*Problem Statement:*
<br/>
In this problem we have a input of n*n length board, current player, value of n and time limit. we have to find the next move of the current player. We used min-max algorithm with alpha-beta pruning to maintain optimization in given time limit.

*Implementation:*
<br/>
To solve this Problem we used minmax algorithm with alpha beta puning. first we made the get_fringe function(Sucessors function). To do this we made 3 functions move_pichu, move_pikachu and move_raichu that for each character finds the valid moves they can make and a get_fringe function that returns a successor list of all possible moves for a given color. Then to get output in time limit we kept increasing the depth of the tree in the find_position() function. Then we assigned value to every node in the tree using a eval() function. Then using min-max algorithm we returned best position for respective depth of the tree.

*Heuristic:*
<br/>
In this Problem we assigned a perticular value to every position in the board. 1 for pichu, 3 for pikachu and 10 for raichu. if the current player is initial player assigned negative value to the heuristic of the state.


*State Space:*
<br/>
A list with all possible moves for raichu, pichu and pikachu for the current player. 

*Sucessor Function:*
<br/>
Pichu can kill by jumping over the other player 2 steps diognally if the space is empty.
pikachu can move 1 or 2 positions on all sides
pikachu can kill by moving 2 or 3 steps on all sides if the final state is empty.
raichu is replaced by current piece if it reaches the other end of the board.
raichu can jump over the other player all over the board and it can move in all directions.
We made all possible combinations for every pichu,pikachu,raichu for the current player to get all sucessors.

*Goal State:*
<br/>
Goal state is a string, The canonical configuration of the board with tiles N*N arranged in a order.

*Challenges:*
<br/>
Creating the 3 move functions for the characters was harder than it seemed because of the time cost to convert the string into an array. As a result movement had to be calculated by adding or subrtacting the position in the string. In order to go up or down the player needed to add N or -N and left and right were -+1. Now the challenges arose when the player could potentailly move left and then wrap around to the other side of the board so many if statements were used checking to see if the position was a multiple of N. Copying and pasting the code for each case resulted in some small errors that were discovered when ran on sharks but for the most part once the moves were ironed out the rest was smooth sailing.


**Part 2 - Truth be Told**

*Problem Statement:*<br />
In this SeekTruth Problem, we are given training and test data on truthful and deceptive hotel reviews. We have to build a Bayesian Classifier that classifies hotel reviews into Truthful and Deceptive. We are using the deceptive.train.txt dataset to train the classifier and we're using the deceptive.test.txt dataset to test the data.<br />

*Implementation:*<br />
After reading the problem statement we took a look at the lecture slides to get some reference on what approach we should follow. We came accross a sum in Probability practice set given by the prrofessor which is something simmilar to this problem. We came up with an approach.
To implement this problem we are using a Probabilistic approach for the bayesian classifier using conditional probabilities. We are calculating probability of the word to be in the spam. It is a classification Problem based on Bayes' Theorem. In simple words we can say that A Bayesian Classifier assumes that a presence of a particular feature is unrelated to the presence of any other features. 
Eg.
    Consider a statement from our sample train dataset and our classifier knows that this is a deceitful review. Our classifier studies the words in this review and many other reviews both truthful and deceitful. It stores words along with their probabilities and then computes the probability of the review to be a spam based on the no of occurences of the words in deceitful reviews. 

*What is Bayes Theorem?*<br />
Bayes' theorem provides a way to compute the posterior probability P(A|B) from P(A), P(B), and P(B|A). Consider the formula: 
<br /> <pre> (P(A|B) = P(B|A)*P(A)/P(B)) </pre>
<br />
Where, <br />
<li>
P(A|B) is the posterior probability of class (A, target) given predictor (B, attributes). <br />
<li>P(A) is the prior probability of class. <br />
<li>P(B|A) is the likelihood which is the probability of predictor given class. <br />
<li>P(B) is the prior probability of predictor. <br />
<br />
Our code is follows this formulae where we calculate, 
<br /><pre> <li> P(A|w1,w2,w2....) </pre>
<br /> <pre><li> P(B|w1,w2,w3....)</pre> <br /> 
Where A is an event where the review is Deceitful and B is the event where the review is Truthful. So, we calculate Threshold which is ratio of 
<pre>
τ = P(A|w1,w2,w2....)/P(B|w1,w2,w3....)
</pre>
Depending on the value of Threshold we can say that the review is Truthful or Deceitful.

*Problems:*<br />
When we implemented this apporoach we faced some issues with the accuracy. When we run the first test out accuracy was about 76%. We tried many things for improving our accuracy and we reached 85.25% accuracy. We cleaned the test data and removed additional data like spaces, coma, etc. One of the problems we faced was what decision should we give when Threshold is equal to 1.
