import sys
#Discussed logic with Dharmik Bhaushali and Vedant Tapadia
#Referenced Youtube videos on n queens backtracking https://youtu.be/xFv_Hl4B83A and https://youtu.be/Ph95IHmRp5M
# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )
# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])
# Add a pichu to the house_map at the given position, and return a new house_map(doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]
def parse_row_right(house_map, r, c):
    for i in range (c+1, len(house_map[0])):
        # print(i)
        if house_map[r][i] == 'p':
            return False
        if house_map[r][i] in 'X':
            break
    # print(i)    
    return True
def parse_row_left(house_map, r, c):
    for i in range (c-1, -1, -1):
        if house_map[r][i] == 'p':
            return False
        if house_map[r][i] in 'X':
            break
    return True
def parse_column_down(house_map, r, c):
    for i in range (r, len(house_map)):
        if house_map[i][c] == 'p':
            return False
        if house_map[i][c] in 'X':
            break
    return True
def parse_column_up(house_map,r,c):
    for i in range (r-1, -1, -1):
        if house_map[i][c] == 'p':
            return False
        if house_map[i][c] in 'X':
            break
    return True

def parse_diag_right_down(house_map,r,c):
    while r< len(house_map) and c < len(house_map[0]):
        if house_map[r][c] == 'p':
            return False
        if house_map[r][c] in 'X':
            break
        else:
            r=r+1
            c=c+1
    return True
def parse_diag_left_down(house_map,r,c):
    while r< len(house_map) and c>= 0:
        if house_map[r][c] == 'p':
            return False
        if house_map[r][c] in 'X':
            break
        else:
            r=r+1
            c=c-1
    return True

def parse_diag_right_up(house_map,r,c):
    while r>=0 and c < len(house_map[0]):
        if house_map[r][c] == 'p':
            return False
        if house_map[r][c] in 'X':
            break
        else:
            r=r-1
            c=c+1

    return True
def parse_diag_left_up(house_map,r,c):
    while r>=0 and c >=0:
        if house_map[r][c] == 'p':
            return False
        if house_map[r][c] in 'X':
            break
        else:
            r=r-1
            c=c-1
    return True

def if_valid (house_map,r,c):
    return parse_row_right(house_map,r,c) and parse_row_left(house_map,r,c) and parse_column_up(house_map,r,c) and parse_column_down(house_map,r,c) and parse_diag_left_down(house_map,r,c) and parse_diag_right_down(house_map,r,c) and parse_diag_left_up(house_map,r,c) and parse_diag_right_up(house_map,r,c)
# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' and if_valid(house_map, r, c)]
# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k
# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    visited= []
    fringe = [initial_house_map]
    while len(fringe) > 0:
        for new_house_map in successors( fringe.pop() ):
            if new_house_map in visited:
                continue
            if is_goal(new_house_map,k):
                return(new_house_map,True)
            if new_house_map not in visited:
                visited.append(new_house_map)
                fringe.append(new_house_map)
    return [], False
# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")