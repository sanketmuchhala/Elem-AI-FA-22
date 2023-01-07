# a0-release
Assignment 1:

Part 1:

Function: parse_map Argument: filename This function takes the "filename" of the input map to create a 2D list in accordance with the map.

Function: valid_index_map Argument: pos, n, m pos = current position; n = row, m = column This function checks if the current position is in bounds of the map.

Function: moves Argument: map, row, col This function finds the possible moves from position (row, col)

Function: assign_dir Argument: move, curr_move, move_string This function assigns a direction to our current position. move_string: indicates the path, consisting of U, L, R, and D characters (for up, left, right, and down) curr_move: current position move: records all the directions

Function: search Argument: house_map

These 5 points are a summarised version of what i understood from the code for the very first time. I firstly thought we would use some shortest path finding algorithm for this problem. I searched google for which algorithms would be best for this problem. BFS and DFS were a common answer for solving such problems. I tried using BFS and I was stuck applying BFS I faced many difficulties applying. I used DFS algorithms for this with the stack implementation. I refered google multiple times for the application of DFS. First it pops all the unwanted nodes and starts exploring childs of pther nodes. When ever it reaches dead end of a node it would backtrack to the parent node and starts exploring other routes. In this way it stores the data for all the routes and in the end suggests the shortest path which would be extracting the smallest value of the path it stored.

Initial State The intial state has a map which represents a map. In this map the path has to begin from p and end at @. In this map '.' denotes free space (i.e free space denotes the way from which we can travel to find the path) and 'X' denotes an obstacle. For Eg consider IUB camppus and we are standing at Indiana Memorial Union Building and we want to travel till Luddy hall the street would be something like '.' and the building are obstacles as while driving a car or a cycle we cannot travel through it. We are using an empty string to store the directions.

Valid State As we discussed in the above example I would like to extend that example to explain valid state. In this problem a valid state is a state from which we can travel ie '.' because it represents road as we talked above. 'X' is not a valid state as we cannot travel through 'X' as it is an obstacle.

Successor Function In the above example for travelling from Indiana Memorial Union to the Luddy hall there are many ways we can take a left from IMU we can go straight from the IMU to reach luddy. We would reach in both ways but whats important is the way which completes least time to reach. That would be efficient in both ways in terms of time and in terms of energy consumed to travel. For the problem our successor function and in example p is the IMU and @ is the luddy hall. Here we are taking a fringe to check if the path is visited previouslyor not. After that we would track the steps taken by the function to real world as left right up or down so we would know where is it going and which path is it taking. For every found valid state we do check if it is visited before or not because if it is visited before we would be wasting time and resources to do that process again. Ad the same process is repeated multiple times.

Cost Function single unit

Goal State The goal state for the example is luddy and for our problem is @. It comes when both our row and our column becomes @. The program showed infite solutions before the path was not getting considered, the path which is to be returned in the ending.


Part 2

#Ref
- 
https://youtu.be/xFv_Hl4B83A 
https://youtu.be/Ph95IHmRp5M


Initial State - The map has walls with an agent and open spaces on a grid.

Goal State - Placing the agents pichus in a way where in none of the conditions i.e. no agent should be in the same row, column or diagonal .

Failed State: If the given number of pichus (agents) cannot be fit in the grid without violating any of the conditions. The program returns false, stating the failure

Approach: While going through the program I could draw similarity between this and n queens problem and hence decided to go through the materials on n queens and chose the back tracking approach, which checks all the rows, columns and diagonals. If the number of pichus could be accommodated on the grid without violating any of the rules the final state reached else the Failed state is returned.

