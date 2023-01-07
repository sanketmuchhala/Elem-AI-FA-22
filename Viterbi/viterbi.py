import copy

# problem definition
states = ("R", "S")
trans = {"R" : {"R": 0.65, "S": 0.35},
         "S" : {"R" : 0.25, "S": 0.75}}
emission = {"R": {"Y" : 0.8, "N" : 0.2},
            "S" : {"Y": 0.2, "N": 0.8}}
initial = {"R": 0.5, "S": 0.5}
observed = ["Y", "N", "Y", "Y", "Y", "Y", "N"]

print("%40s: %s " % ("Observed sequence", str(observed)))

N=len(observed)

###########################
# We can find the most likely state sequence in a brute-force way by just
# trying all of them!

joint = {}
for s0 in states:
    for s1 in states:
        for s2 in states:
            for s3 in states:
                for s4 in states:
                    for s5 in states:
                        for s6 in states:
                            seq = str([s0, s1, s2, s3, s4, s5, s6])
                            joint[seq] = initial[s0]*trans[s1][s0]*emission[s1]['N']*trans[s2][s1]*emission[s2]['Y']*trans[s3][s2]*emission[s3]['Y']*trans[s4][s3]*emission[s4]['Y']*trans[s5][s4]*emission[s5]['Y']*trans[s6][s5]*emission[s6]['Y']

                            # FILL THIS IN by computing P(S0...S6 | O0...O6)
                            # Hint: Since P(S0...S6 | O0...O6) = P(S0...S6,O0...O6) / P(O0...O6),
                            #   but P(O0...O6) is fixed by the problem and a positive number,
                            #   maximizing P(S0...S6,O0...O6) is the same as maximizing P(S0...S6 | O0...O6).
                            #   So just compute the joint probability P(S0...S6,O0...O6)  instead


print("%40s: %s" % ("Most likely sequence by brute force:", str(max(joint, key=joint.get))))

#############################
# obviously that's a big mess, and slow -- each every day requires another nested loop and 2x the computation time.
# so instead, compute using Viterbi!

# Viterbi table will have two rows and N columns
V_table = {"R": [0] * N, "S" : [0] * N}


# Here you'll have a loop to build up the viterbi table, left to right
V_table["R"][0] = initial["R"]
V_table["S"][0] = initial["S"]
for i in range(1,N):
    R_max = max(V_table["R"][i-1]*trans["R"]["R"], V_table["S"][i-1]*trans["S"]["R"])
    S_max = max(V_table["R"][i-1]*trans["R"]["S"], V_table["S"][i-1]*trans["S"]["S"])
   
    V_table["R"][i] = emission["R"][observed[i]]*R_max
    V_table["S"][i] = emission["S"][observed[i]]*S_max
   

# Here you'll have a loop that backtracks to find the most likely state sequence
viterbi_seq = ["M"] * N
for i in range(N):
    if V_table["R"][i] > V_table["S"][i]:
        viterbi_seq[i] = "R"
    else:
        viterbi_seq[i] = "S"



 # remove this and put your answer in here instead
print("%40s: %s" % ("Most likely sequence by Viterbi:", str(viterbi_seq)))