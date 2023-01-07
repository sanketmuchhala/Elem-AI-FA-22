# samuch-rifhall-akukkapa1-a3
Elements of AI - Assignment 3 - Probability, NLP, and Computer Vision


# Part1 - Part-of-speech tagging
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
These three techniques are being used for speech tagging.
1. Naive bayes 
2. Gibbs Sampling with MCMC
3. Viterbi Algorithm 
## Labelling for the Input
<img width="100%" alt="Screenshot_20221205_074216" src="https://media.github.iu.edu/user/20661/files/b8a0569a-d8ca-41d9-ab0b-04a9de0e1ceb">

## Simplified Model
In the Simplified model, we just looked at the relationship between the components of speech and the words.
Formulation: 

$P(S|W) = max{P(W|S)\, P(S) \over P(W)}$

For each word in the phrase, we maximize the posterior probability P(S|W) probability of part-of-speech given the word, i.e. Prior * Likelihood (P(S) * P(W|S)).
The overall accuracy for this strategy was 91.51% for words and 36.35% for phrases.


## Complex Markov Chain Monte Carlo using Gibbs Sampling
In this technique, transition probabilities from the third word in a sentence to two preceding portions of speech must be examined.

For example, P(noun, det, verb) is formed from the dict[noun][det][verb]. In the lack of probability information for a certain sequence, a minimum probability (in our instance 1e-10) for calculation feasibility is provided.

S(n) is the Parts-of-Speech tag for the nth word in a sentence, and S(n-1), S(n-2) are the Parts-of-Speech tags for the cells below. We will be able to easily
determine transition probability by simply accessing relevant keys in the dictionary.

We have created a table P(Sn/Sn-1,S1) for the calculation of Gibbs sampling in order to sample values from the posterior distribution.

1. P(S1) is proportional to P(S1)*P(S2/S1)*P(W1/S1)*P(Sn/Sn-1,S1)
2. P(Sn) is proportional to P(Wn/Sn)*P(Sn/Sn-1,S1)
3. P(Sn-1) is proportional to P(Wn-1/Sn-1) *P(Sn/Sn-1,S1) *P(Sn-1/Sn-2)

Many samples must be created in order to generate part of speech tags for each word in the phrase. When the sample size was increased from 100 to 2000, the prediction accuracy did not change appreciably. We employ word predictions from HMM for this, and we believe this is a better strategy with a larger possibility of convergence in less time.

The distribution is used to choose a tag for the current word, which is subsequently altered for the next sample. The next sample will be generated using this improved version.

The overall accuracy for this strategy was 95.05% for words and 54.45% for phrases.

## Hidden Markov Model using Viterbi Algorithm
Unlike previous models, this one considers both the reliance on consecutive words and the dependency on word to sentence.

Keeping track of the maximum probabilities until the probabilities of each word in a phrase are determined is part of our procedure, and we use the maximum probability of the preceding word, which is precalculated. To make the data more accessible for calculation, we constructed the transition matrix.

The overall accuracy for this strategy was 93.98% for words and 48.70% for phrases.

## Output
<img width="405" alt="image" src="https://media.github.iu.edu/user/20661/files/1586e296-7ce7-405b-b3bb-f4d3a4c96cda">

# Part2 - Reading text
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Problem:
</br>The characters in this question are all represented by stars (*) and spaces (), and our task is to identify them from the image. We have two algorithms to use.
1. Simple Bayes Net
2. HMM 

Training Phase:
</br>As for this statement we were provided with a training image to train the model. That image is basicallly an Image version of the training text given in the runner code. 
</br>Calculating Transition Probability:
</br>Probability that a chararecter is followed by another chararecter and this is done using training file.
</br>Calculating Emission Probability:
</br>Probability for simmilar test and train chararecter.
</br>Now we apply Naive Bayes on it.

## Simple Bayes Nets
For each test character in the Bayes network, we simply return the corresponding train character with the highest emission probability.</br>
in other words Simple Bayes Nets Implementation, we first store the dictionarys actual letters and values in a separate list together with their key words associated with them. We received one sample image with correct representations of each character to use as training data. This list of patterns was used to train the algorithm. We create the following heuristic to train the algorithm. And another list will be added to that one.  After that, the star locations for each testing letter (for each row) will be compared to the star locations for each character (from the training data), and for each match, one count will be added to the list. As a result, we will obtain a list of lists for the number of matches for each character in the data set. which will change to P(Oi | Li), which is the probability of pater given a specific character. Therefore, we will have the likelihood that each pattern exists, and the maximum values will be assigned to the dictionary's keys.

## HMM
Basically, Initial Probability, Emission Probability, and Transition Probability are required for the use of HMM. Initial Probability: To begin, we combined each sentence in a text data set into a tuple (name of which was V). From there, we were able to extract the first letters of each sentence, which we then stored in a list. We then calculated the frequency of each letter in the list by dividing it by the total number of initial letters. I was able to determine each letter's initial probability in this way.</br>
Emission Probability:</br>
It is the probability of observation of network event data conditioned on the state of the mobile device, in a dynamical approach based on a hidden Markov model.
</br>Transition Probability:
</br>It is the probability of moving from one state of a system into another state.
