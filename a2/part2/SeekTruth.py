# SeekTruth.py : Classify text objects into two categories
#
# Code by: Sanket Muchhala, Abhiram Kukkapali, Haloran Riley
#
# Based on skeleton code by D. Crandall, October 2021
#
#Mark 47

import sys

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")
            
    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    dict1 = dict()
    for i in range(len(train_data["objects"])):
        line = train_data["objects"][i]  # reading the reviews line by line
        count1 = line.replace(',', '').replace('**','').replace('*','').replace('!','').replace('-','').strip().lower().split()
        for word in count1:
            if word not in dict1:
                dict1[word]=[0,0]
            if train_data["labels"][i] == "truthful":
                dict1[word][0]+=1
            else:
                dict1[word][1]+=1
    #print(dict1)
    
    result = []  
    for i in range(len(test_data['objects'])):
        line = test_data['objects'][i] 
        count_tru=1
        count_dec=1
        for word in line.replace(',', '').replace(".", '').replace('**','').replace('(','').replace(')','').replace('*','').replace('!','').replace('$','').strip().lower().split():
            if word not in dict1:
                continue  
            else:
                if 0 in dict1[word]:
                    if dict1[word][1]==0 and dict1[word][0]>2:
                        count_tru= count_tru* dict1[word][0]
                    elif dict1[word][0]==0 and dict1[word][1]>2:
                        count_dec=count_dec* dict1[word][1]
                else:
                    if dict1[word][0]>1:
                        if dict1[word][1]>1:
                            count_tru=count_tru*(dict1[word][0]/(dict1[word][0]+dict1[word][1]))
                            count_dec=count_dec*(dict1[word][1]/(dict1[word][0]+dict1[word][1]))
        if (count_tru/count_dec>1):  # if probability is > 1, then truthful will be appended in result
            result.append('truthful')
        else:  # if probability is < 1, then deceptive will be appended in result
            result.append('deceptive')
    return result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
