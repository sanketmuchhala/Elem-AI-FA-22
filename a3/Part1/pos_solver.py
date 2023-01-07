###################################
# CS B551 Fall 2022, Assignment #3
#
# Code by: Abhiram Kukkapali, Sanket Muchhala, Haloran Riley
#
# (Based on skeleton code by D. Crandall)
#

import random
import math


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.

class Solver:
    def __init__(self):
        self.ver_table = [{}]
        self.emission_prob_gobal = {}
        self.transition_prob_global = {}
        self.transition2_prob_global = {}
        self.emission_count_global = {}
        self.transition_count_global = {}
        self.transition2_global = {}
        self.global_initial_count = {}
        self.unique_parts_global = []
    def posterior(self, model, sentence, label):
        words = list(sentence)
        value = list(label)
        if model == "Simple":
            p = 0
            for i in range(len(words)):
                p += math.log10(self.emission_probability(words[i], value[i])) + \
                     math.log10(self.global_initial_count[value[i]] / sum(
                         self.global_initial_count.values()))
            return p
        elif model == "Complex":
            s1 = value[0]
            prob_s1 = math.log(
                self.global_initial_count[s1] / sum(self.global_initial_count.values()), 10)
            p1, p2, p3 = 0, 0, 0
            for i in range(len(value)):
                p1 += math.log(self.emission_probability(words[i], value[i]), 10)
                if i != 0:
                    p1 += math.log(self.get_transition_probability(value[i - 1], value[i]), 10)
                if i != 0 and i != 1:
                    p3 += math.log(self.get_2nd_level_trans_prob(value[i - 2], value[i - 1], value[i]), 10)
            return prob_s1 + p1 + p2 + p3
        elif model == "HMM":
            prob_s1 = math.log(self.global_initial_count[value[0]] / sum(
                self.global_initial_count.values()), 10)
            p1, p2 = 0, 0
            for i in range(len(value)):
                p1 += math.log(self.emission_probability(words[i], value[i]), 10)
                if i != 0:
                    p2 += math.log(self.get_transition_probability(value[i - 1], value[i]), 10)
            return prob_s1 + p1 + p2
        else:
            print("Unknown algo!")

    def emission_probability(self, word, value):
        if word in self.emission_prob_gobal and value in self.emission_prob_gobal[word]:
            return self.emission_prob_gobal[word][value]
        if word in self.emission_count_global and value in self.emission_count_global[
            word] and value in self.transition_count_global:
            value = self.emission_count_global[word][value] / sum(self.transition_count_global[value].values())
            self.emission_prob_gobal[word] = {value: value}
            return value
        return 0.00000001

    def initial_probability(self, value):
        if value in self.global_initial_count:
            return self.global_initial_count[value] / sum(
                self.global_initial_count.values())
        return 0.00000001

    # Do the training!
    #
    def train(self, train_file):
        previous_value = None
        before_the_previous_value = None
        for words, parts_of_speech in train_file:
            word_length = len(words)
            if parts_of_speech[0] in self.global_initial_count:
                self.global_initial_count[parts_of_speech[0]] = self.global_initial_count[parts_of_speech[0]] + 1
            else:
                self.global_initial_count[parts_of_speech[0]] = 1
            for i in range(word_length):
                if words[i] in self.emission_count_global:
                    if parts_of_speech[i] in self.emission_count_global[words[i]]:
                        self.emission_count_global[words[i]][parts_of_speech[i]] = self.emission_count_global[words[i]][
                                                                                parts_of_speech[i]] + 1
                    else:
                        self.emission_count_global[words[i]][parts_of_speech[i]] = 1
                else:
                    self.emission_count_global[words[i]] = {parts_of_speech[i]: 1}

                if not previous_value is None:
                    if previous_value in self.transition_count_global:
                        if parts_of_speech[i] in self.transition_count_global[previous_value]:
                            self.transition_count_global[previous_value][parts_of_speech[i]] = \
                            self.transition_count_global[previous_value][
                                parts_of_speech[i]] + 1
                        else:
                            self.transition_count_global[previous_value][parts_of_speech[i]] = 1
                    else:
                        self.transition_count_global[previous_value] = {parts_of_speech[i]: 1}

                if (before_the_previous_value and previous_value) is not None:
                    if before_the_previous_value in self.transition2_global:
                        if previous_value in self.transition2_global[before_the_previous_value]:
                            if parts_of_speech[i] in \
                                    self.transition2_global[before_the_previous_value][
                                        previous_value]:
                                self.transition2_global[before_the_previous_value][
                                    previous_value][parts_of_speech[i]] = \
                                    self.transition2_global[before_the_previous_value][
                                        previous_value][parts_of_speech[i]] + 1
                            else:
                                self.transition2_global[before_the_previous_value][
                                    previous_value][parts_of_speech[i]] = 1
                        else:
                            self.transition2_global[before_the_previous_value][
                                previous_value] = {parts_of_speech[i]: 1}
                    else:
                        self.transition2_global[before_the_previous_value] = {
                            previous_value: {parts_of_speech[i]: 1}}
                previous_value = parts_of_speech[i]

                try:
                    before_the_previous_value = parts_of_speech[i - 1]
                except IndexError:
                    before_the_previous_value = None

        self.unique_parts_global = list(self.transition_count_global.keys())


    def simplified(self, words):
        tags_list = [''] * len(words)
        for j in range(len(words)):
            p = 0
            for i in range(len(self.unique_parts_global)):
                tag = self.unique_parts_global[i]
                p_new = self.emission_probability(words[j], tag) * self.initial_probability(tag)
                if p_new > p:
                    tags_list[j] = tag
                    p = p_new
        return tags_list

    def get_transition_probability(self, value1, value2):
        if value1 in self.transition_prob_global and value2 in self.transition_prob_global[value1]:
            return self.transition_prob_global[value1][value2]

        if value1 in self.transition_count_global and value2 in self.transition_count_global[value1] and value2 in self.transition_count_global:
            value = self.transition_count_global[value1][value2] / sum(self.transition_count_global[value1].values())
            return value
        return 0.0000001

    def get_2nd_level_trans_prob(self, pos1, pos2, pos3):

        if pos1 in self.transition2_prob_global and pos2 in self.transition2_prob_global[pos1] and pos3 in self.transition2_prob_global[pos1][pos2]:
            return self.transition2_prob_global[pos1][pos2][pos3]
        if pos1 in self.transition2_global and pos2 in self.transition2_global[pos1] and pos3 in self.transition2_global[pos1][pos2]:
            value = self.transition2_global[pos1][pos2][pos3] / sum(self.transition2_global[pos1][pos2].values())
            self.transition2_prob_global[pos1] = {pos2: {pos3: value}}
            return value
        return 0.00000001


    def complex_mcmc(self, words):
        samples = []
        count_tags_array = []
        sample = self.simplified(words)
        iterations = 25
        burning_iteration = 10
        for i in range(iterations):
            tags = list(self.global_initial_count.keys())
            for index in range(len(words)):
                probability_array = [0] * len(tags)
                log_probability_array = [0] * len(tags)
                for j in range(len(tags)):
                    sample[index] = tags[j]
                    s1 = sample[0]
                    prob_s1 = math.log(
                        self.global_initial_count[s1] / sum(
                            self.global_initial_count.values()), 10)
                    t, z, r = 0, 0, 0
                    for k in range(len(sample)):
                        z += math.log(self.emission_probability(words[k], sample[k]), 10)
                        if k != 0:
                            t += math.log(self.get_transition_probability(sample[k - 1], sample[k]), 10)
                        if k != 0 and k != 1:
                            r += math.log(self.get_2nd_level_trans_prob(sample[k - 2], sample[k - 1], sample[k]), 10)
                    log_probability_array[j] = prob_s1 + t + z + r

                a = min(log_probability_array)
                for k in range(len(log_probability_array)):
                    log_probability_array[k] -= a
                    probability_array[k] = math.pow(10, log_probability_array[k])
                s = sum(probability_array)
                probability_array = [x / s for x in probability_array]
                rand = random.random()
                p = 0
                for k in range(len(probability_array)):
                    p += probability_array[k]
                    if rand < p:
                        sample[index] = tags[k]
                        break
            if i >= burning_iteration:
                samples.append(sample)
        for j in range(len(words)):
            count_tags = {}
            for sample in samples:
                try:
                    count_tags[sample[j]] += 1
                except KeyError:
                    count_tags[sample[j]] = 1
            count_tags_array.append(count_tags)
        final_tags = [max(count_tags_array[i], key=count_tags_array[i].get) for i in range(len(words))]
        return [tag.lower() for tag in final_tags]

    def hmm_viterbi(self, words):
        self.ver_table = [{}]
        viterbi_track = {}
        for i in self.unique_parts_global:
            self.ver_table[0][i] = self.initial_probability(i) * self.emission_probability(words[0], i)
            viterbi_track[i] = [i]
        for i in range(1, len(words)):
            self.ver_table.append({})
            current_path = {}
            for current_pos in self.unique_parts_global:
                max_value = 0
                for pre_pos in self.unique_parts_global:
                    value = self.ver_table[i - 1][pre_pos] * self.get_transition_probability(pre_pos,current_pos) * self.emission_probability(words[i], current_pos)
                    if value > max_value:
                        max_value = value
                        state = pre_pos
                self.ver_table[i][current_pos] = max_value
                current_path[current_pos] = viterbi_track[state] + [current_pos]
            viterbi_track = current_path
        max_value = -math.inf
        last_level = len(words) - 1
        for i in self.unique_parts_global:
            if self.ver_table[last_level][i] >= max_value:
                max_value = self.ver_table[last_level][i]
                best_state = i
        state = best_state
        return viterbi_track[state]


    def solve(self, model, sentence):
        words = list(sentence)
        if model == "Simple":
            return self.simplified(words)
        elif model == "Complex":
            return self.complex_mcmc(words)
        elif model == "HMM":
            return self.hmm_viterbi(words)
        else:
            print("Unknown algo!")
