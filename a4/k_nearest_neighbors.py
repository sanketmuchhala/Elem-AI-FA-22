# k_nearest_neighbors.py: Machine learning implementation of a K-Nearest Neighbors classifier from scratch.
#
# Submitted by: Sanket Muchhala -- samuch
#
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

import numpy as np
from utils import euclidean_distance, manhattan_distance

class KNearestNeighbors:
    """
    A class representing the machine learning implementation of a K-Nearest Neighbors classifier from scratch.

    Attributes:
        n_neighbors
            An integer representing the number of neighbors a sample is compared with when predicting target class
            values.

        weights
            A string representing the weight function used when predicting target class values. The possible options are
            {'uniform', 'distance'}.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model and
            predicting target class values.

        _y
            A numpy array of shape (n_samples,) representing the true class values for each sample in the input data
            used when fitting the model and predicting target class values.

        _distance
            An attribute representing which distance metric is used to calculate distances between samples. This is set
            when creating the object to either the euclidean_distance or manhattan_distance functions defined in
            utils.py based on what argument is passed into the metric parameter of the class.

    Methods:
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_neighbors = 5, weights = 'uniform', metric = 'l2'):
        # Check if the provided arguments are valid
        if weights not in ['uniform', 'distance'] or metric not in ['l1', 'l2'] or not isinstance(n_neighbors, int):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the KNearestNeighbors model object
        self.n_neighbors = n_neighbors
        self.weights = weights
        self._X = None
        self._y = None
        self._distance = euclidean_distance if metric == 'l2' else manhattan_distance

    #This method takes training data
    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        #Setting 2 Training variables TX and Ty 
        #In KNN we just store the training data thats why KNN is lazy learners Algoroithm 
        self._X = X
        self._y = y
        # raise NotImplementedError('This function must be implemented by the student.')

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        #Took Reference from https://towardsdatascience.com/k-nearest-neighbors-classification-from-scratch-with-numpy-cb222ecfeac1
        # and https://medium.com/analytics-vidhya/implementing-k-nearest-neighbours-knn-without-using-scikit-learn-3905b4decc3c
        # and https://iu.instructure.com/courses/2081806/files/148750599?module_item_id=28310382
        arr = []
        n = len(X)
        Y = self._y
        weights = self.weights
        
        for i in range (n):
            distance = []
            v = []
            for j in range (n):
                distance.append([euclidean_distance(X[j], X[i]),j])
            distance.sort()
            cd = {}
            
            #Updating only distance till n_neighbour
            def till_n_neighbor(distance):
                return distance[:self.n_neighbors]
            
            dis = till_n_neighbor(distance)
            if weights == 'uniform':
                for _, j in dis:
                    v.append(Y[j])
                counterr = {}
                v = [str(x) for x in v]
                for w in v:
                    counterr[w] = counterr.get(w, 0) + 1
                ai = list(counterr.values())
                tmp = list(counterr.keys())[list(counterr.values()).index(max(ai))]
                arr.append(tmp)
            #Computing for distance
            else:
                uv = []
                for x in Y:
                    if x not in uv:
                        uv.append(x)
                for k in range(len(uv)):
                    cd[uv[k]] = 0
                for dist,index in dis:
                    if dist == 0:
                        cd[Y[index]]+=1
                    else:
                        cd[Y[index]]+=1/dist
                arr.append(max(cd,key=cd.get))
        return arr
        # raise NotImplementedError('This function must be implemented by the student.')