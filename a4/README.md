# samuch - a4
## Assignment 4 - Machine Learning

#### Part 1 -  K-Nearest Neighbors Classification

In the problem statement we were given to implement K-Nearest Neighbours Classification from scatch in Python3 using numpy. </br>
The K-nearest neighbor Algorithm is used, with some minor modification that when the parameter is set to "distance," the weights for taking into account the nearest points should be proportional to the inverse of the distance from the test sample to each neighbor, as opposed to the typical straight proportional distance.

##### Utils.py
</br>For KNN we are calculating manhattan distance and euclidian distance in Utils.py</br>
</br>Euclidean Distance: 
</br> It is a measure of the true straight line distance between two points. In simple words it is distance between x2 and x1. </br>Formulae: </br><pre>sqrt(sum(square(x1-x2)))</pre>
</br>Manhattan Distance:
</br>  The distance between two points is the sum of the absolute differences of their Cartesian coordinates. </br>Formulae: </br><pre>sum(|x1-x2|)</pre>

##### k_nearest_neighbours.py
</br>fit(X,y):
</br>Fits the model to the provided data matrix X and targets y. In this function we are defining self.X and self.Y which are the values of X and Y.
</br>predict(X):
</br>The simplest supervised approach is K nearest neighbors, which is used to discover patterns. Using this method we examine the test data to determine how similar it is to a particular group in terms of the Gaussian distribution of the training data.
</br>Comparing the precision of our method to the precision of the Sklearn package. The manhattan and euclidean distance calculations are simple arithmetic operations, therefore I used the numpy library. By evaluating the test and train datasets, it is possible to figure out which category the data belongs to with the predict method. I assisted as I was asked to utilize the inverse of the distance if the weight = "distance."
</br>Lets have alook at the accuracy. 

##### Problems: 

#### Part 2 - Multilayer Perceptrol Classification 

In the problem statement we were given to implement Multilayer PEreptron Classification from scatch in Python3 using numpy. Testing on Iris and digit dataset in scikit learn library.

##### Utils.py
</br>Identify:
</br>Computes and returns the identity activation function of the given input data x. 
 </br>Sigmoid:
 </br>Computes and returns the sigmoid (logistic) activation function of the given input data x.
 </br>tanh:
 </br>Computes and returns the hyperbolic tangent activation function of the given input data x.
 </br>Relu:
 </br>Computes and returns the rectified linear unit activation function of the given input data x.
 </br>Cross entrophy:
 </br>Computes and returns the cross-entropy loss, defined as the negative log-likelihood of a logistic model that returns p probabilities for its true class labels y.
 </br>One hot encoding 
 </br> Converts a vector y of categorical target class values into a one-hot numeric array using one-hot encoding: one-hot encoding creates new binary-valued columns, each of which indicate the presence of each possible value from the original data.
 
##### multilayer_perceptron.py

</br>Initialize:
</br> unction called at the beginning of fit(X, y) that performs one hot encoding for the target class values and initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).
</br> self.X is X same as in kNN and y is one_hot_encoded
</br>Firt:
</br>Fits the model to the provided data matrix X and targets y and stores the cross-entropy loss every 20 iterations.
