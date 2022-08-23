
# Part 1: The 2021 Puzzle
Find a short sequence of moves that restores the canonical configuration by only moving tiles as per the allowed moves (given constraints) from the initial state.

### State Space/Valid States:
Set of all valid states wherein 25 tiles (numbered 1-25) could be placed.

### Initial State: 
Initial boards provided wherein all 25 tiles are placed randomly.

### Successor Function: 
There are 24 successor function (next possible move for current state) that are possible for every board in this problem.  These are based on move constraints given for row, column, inner-circle and outer-circle of board.

The next possible moves are obtained by performing certain operations on rows, columns, inner and outer elements of the board.
* Slide row one tile to the right, "wrapping around to the other side of the board" -  5 moves for all 5 rows
* Slide row one tile to the left, "wrapping around to the other side of the board" – 5 moves for all 5 rows
* Slide column one tile upwards, "wrapping around to the other side of the board" – 5 moves for all 5 columns
* Slide column one tile downwards, "wrapping around to the other side of the board" – 5 moves for all 5 columns
* Slide outer circle clockwise rotation – 1 move
* Slide outer circle counter-clockwise rotation – 1 move
* Slide inner circle clockwise rotation – 1 move
* Slide inner circle counter-clockwise rotation – 1 move
In order to move any tile, all these moves (successors) need to be evaluated.

### Goal State: 
The goal state is when all tiles are placed in the order of 1-25 values on the board.

## Approach Taken:
We have implemented A* algorithm, as this will prioritize the states that are much more likely to be closer to the goal state than the other states by taking the least expensive path. Hence, the better the estimate the more efficient the search. A* uses: * Admissible Heuristic Function, * Right evaluation function, * Best First search

### Cost Function: Evaluation function "f_score = g_score + h_score" calculates the cost to reach the goal position 
The g_score that we've considered for this problem basis the weight of the edges is 1, regardless of what state is considered. 
The h_score which is the heuristic function, we tried to implement both Manhattan distance and Number of misplaced tiles heuristic for this problem but neither of them turned out to be more admissible than the other and lead to a similar output for both the test cases. So we implemented the seacrh with the number of msipalced tiles heuristic (although implementation of the manhattan distance heuristic is still there in the code)

### Search:
All valid states are added to the fringe calculating the best cost and for the state and move along as it is traversed, the fringe stores the heuristic function for each move. It is then sorted based on the heuristic values and evaluation function in ascending order so we can pop the first element and assign that state to the current move which gets checked for the goal state. 


### Difficulties faced:
* We tried implementing the heuristics (h1) sum of misplaced tiles and (h2) Manhattan distances, although we realized that neither of them are admissible for the wrap around and rotation moves, although they were admissible for the other moves. For the most part we tried implementing Manhattan by dividing the final values by 5 for vertical and horizontal moves, by 8 for inner clockwise or counter-clockwise moves and by 16 for outer-clockwise or counter-clockwise moves. Although this still didn't give a heuristic that would be admissible for this problem statement.

## Questions:
#### In this problem, what is the branching factor of the search tree?
The branch factor for the search tree would be 24, as every node would have 24 moves that could be made next in order to go to the next possible state in our path to reaching the goal state.
#### If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search? A rough answer is fine.
The advantage of A* is that would expand far fewer nodes as compared to BFS, it would take in a priority queue to check which move should be taken basis the cost function and only the successor that has the least cost is explored. So if A* is implemented and 7 moves are explored, then for BFS at least 24^7 states would need to be explored to reach our goal state.



---------------------------------------------------------------------------------------


# Part 2: Road Trip!
The aim is to find an optimal path between two cities meaning that we have to find good driving directions between pairs of cities.

### State Space/Valid states:
To find all successive neighbouring cities which are reachable from a given particular city. In otherwords, to be able to check whether a given state for a particular instance is valid or not. 

### Initial State
Start city is the initial state. For example, if we have to start from "Bloomington,_Indiana" to "Indianapolis,_Indiana", the initial state is "Bloomington,_Indiana".

### Successor Function
To find all successive neighbouring cities for a given particular city. In this particular problem, state space would be all the possible next cities that can be  traversed from the current city. Which in other words, means all the successors(next cities) of the current city. We generate successors for each city(node) until we reach the goal node.

* Firstly, we generate all the successors for a given particular city. 
* Secondly, calculating heuristic value for each city to know which city to traverse next so that we can get the optimal route to the destination. The shorter the value, the most optimal is the route.
* All of these successors are generated and once explored, we are appending it to the visited list in order to reduce the time and space complexity such that no city that has already been visited will be appended to the fringe again and again.

### Goal State
The final destination that we want to reach which in this example will be "Indianapolis,_Indiana".

### Cost Function:
 Evaluation function f(s) = g(s) + h(s) calculates the cost at every step and only takes the least cost path to reach the goal position.
 * f(s) is the total cost
 * g(s) is the actual cost from the beginning of the node
 * h(s) is the heuristic function is an underestimate because it is less than or equal to the lowest possible cost from node current point n to goal g. In          otherwords, h_score never over estimates the cost of reaching the goal.
 
* Next city/successor is chosen based on the value of heuristic functions. Calculating the heuristic function(cost) for each of these below-

    * cost == distance
    	g(s) - the distance travelled so far from the beginning of the path
        h(s) - calculating distance using "The haversine formula" which computes the accurate distance between two points on a sphere given their longitudes and latitudes. This calculates the distance between all the next cities to the goal state so that the current city can choose the shortest path amongst these based on the heuristic value returned in the fringe.
	
    * cost == segments 
    	g(s) - the segment length traversed until now or the number of segments(length between two cities is considered as segment length).
        h(s) - the heuristic distance divided by maximum segment length so that the heuristic never over estiamtes the actual segment length. If heuristic is admissible, it never over estimates the cost function. 
	
    * cost == time 
    	g(s) - the time travelled so far from the beginning 
        h(s) - the heuristic distance(haversine formula) divided by maximum speed limit so that the heuristic is admissible. For example, the maximum speed given in the dataset is 10 and say haversine distance is 50. The time we get is distance/speed = 5. So, the heuristic should never over estimate the actual time taken to travel that particular path. Actual time is when we compute the actual distance between those two cities and speed limit for that path. That's when we say our heuristic is admissible. So, by diving with max_speed_limit, we can never overestimate the cost of reaching goal.
	     
    * cost == delivery 
    	g(s) - the time taken to travel the path. If the speed limit is greater than 50 mph for a particular path between two cities, the delivery person is most           likely to drop a packet which in case we're calculating the given formula "t_road + p * 2 * (t_road + t_trip)" 
          Otherwise, just calculating the time travelled so far plus the time of the current road segment.
	h(s) - haversine distance divided by time so that this time never over estimates the actual time taken to travel the de-tour if the delivery person drops a 	           packet

    * other_delivery - This isn't a heuristic function but it calculates thes actual time taken to travel if the speed exceeds 50mph.

### Search:
Based on the cost function as "segments" or "distance" or "time" or "delivery" given in the command line argument, the particular cost function gets called and evaluates the cost based on the heuristic function. We have used heapq module to implement priority queues. The property of this heap data structure in Python is that each time the smallest of heap element is popped from the fringe. The reason for using this heap module is because whenever elements are pushed or popped, heap structure is maintained. Fringe stores heuristic values for each step so the least value gets popped each time. The heapq.heappop(fringe) pops the smallest element each time and that's how we are getting the best route based on the cost. 

### Difficulties Faced:
* While the conceptualization and the ideation phases of this problem seemed fairly easy, the implementation and realization of the task via a program was much difficult than anticipation.
* Validation of the solution: Debugging and verifying that the solution is fail-safe was a monumental job due to the restricted amount of test cases and the difficulty of producing another test case. As a result, the solution's validation took longer. It also necessitated advanced python knowledge and drove us all to examine the problem statement, code, and accessible test case for probable areas of failure.

-----------------------------------------------------------------------------------------
# Part 3: Choosing Teams

### Initial Analysis/Simplifying the problem

    Task    :   To form teams with least cost satisfying all conditions.
    inputs  :   text file with each line consisting of
                username teammates-requested dont-want-to-work-with,people
                
                djcran djcran-vkvats-nthakurd sahmaini
                sahmaini sahmaini _
                sulagaop sulagaop-xxx-xxx _
                fanjun fanjun-xxx nthakurd
                nthakurd nthakurd djcran,fanjun
                vkvats vkvats-sahmaini _

    Cost    : 
            action                  cause                                               cost
        
            grading                                                                     5 mins
            mail to professor       incorrect team size                                 2 mins
            integrity session       sharing code (different teammate than requested)    5% probability and 60 mins - 3mins 
            speaking with Dean      when teamed with dont-want-to-work-with                           10 mins


### Formulating a "Search Problem"

Search Abstraction: (Used "Local" Search with slight modifications in the due process)

    * Initial State: All Students divided into groups of 3( N/3 groups)

    * Goal State: Assigning teams which take least amount of instructors time while satisfying the constraints of the individual

    * Successor Function: List of all "worthy teams" for each individual which puts least load on the instructor.

    * State Space: List of all "worthy teams" for each individual (Worthy team is a team made of 'worthy people')

    * Cost function: 
        action                  cause                                               cost

        grading                                                                     5 mins
        mail to professor       incorrect team size                                 2 mins
        integrity session       sharing code (different teammate than requested)    5% probability and 60 mins - 3mins
        speaking with Dean      when teamed with dont-want-to-work-with             10 mins


### How our solution works: 

1. Yield a random solution
2. Finds list of all "worthy" users for each user.
  - A worthy individual is someone who is not on "dont-want-to-work-with" list of the current user, and the current user is not in the "dont-want-to-work-with-list" of the other user

3. Generating combinations of team size - 3, 2 and 1 - of all "worthy" teams in "worthy-list" of each indivudal 

4. Finding teams that are of low cost that form an efficient solution and yielding them

### Other solutions tried	
- Tried to split and combine after random results
- Tried just picking random individuals from all users
- Tried to pick combinations of 3,2 and 1 user teams to find ideal solution
- Tried randomizing the `worthy-teams`
- Tried building trees for each user

### Why this approach

  - First idea was to form random/quick solutions and then to split the teams and then to combine them.
  - Another approach (most followed) was random team generation.
	  - While this approach might get a the solutions quick, it does not account for a formal search of the search space.
	  - Even if it is possible to cover the entire search space, the search space is very exhaustive.
	  - Following the approach of worthy-teams yields a definitive set of teams from which a search is definite to produce the most optimal outputs. 
  - Instead the current approach limits the total number of "dean-interactions" thus directly reducing the over-all cost, because, dean interactions are the costliest of all kinds - 10 mins.
	  - The first yield happens very quickly
	  - Thrives on optimistic apporach to the solutions
	  - Has a finite defined state-space.
  - totally object oriented program with a pylint score of 9.49/10.0
		```

		(venv) C:\Users\Asus\Downloads\nsadhuva-adisoni-svaddi-a1-master (1)\nsadhuva-adisoni-svaddi-a1-master\part3>pylint -d C0301,R1719,C0325 assign.py
		************* Module assign
		assign.py:72:8: R1705: Unnecessary "else" after "return" (no-else-return)
		assign.py:118:11: R1729: Use a generator instead 'any(True for j in team.current_team if j in all_user_dict[i].dont_want_to_work_with)' (use-a-generator)
		assign.py:134:0: R0902: Too many instance attributes (16/7) (too-many-instance-attributes)
		assign.py:140:4: W0102: Dangerous default value [] as argument (dangerous-default-value)
		assign.py:306:4: W0102: Dangerous default value [] as argument (dangerous-default-value)
		assign.py:325:8: R1703: The if statement can be replaced with 'return bool(test)' (simplifiable-if-statement)
		assign.py:325:8: R1705: Unnecessary "else" after "return" (no-else-return)
		assign.py:354:12: W0106: Expression "[self.users.append(j) for j in i.current_team]" is assigned to nothing (expression-not-assigned)
		assign.py:403:12: R1724: Unnecessary "else" after "continue" (no-else-continue)
		assign.py:376:0: R0912: Too many branches (16/12) (too-many-branches)
		-----------------------------------
		Your code has been rated at 9.49/10
		
		```
### Doubts/Issues : 

- Is it complete? 
- If it is, can it yield a solution in any number of iterations and any amount of time ?
- Is it optimal? 
- Time taken for execution?
- Is it the same solution? 
  - if the algo produces same groups over and over again
      - can happen if the formation of a particular group causes the tree to flow down same path

### Challenges

- While the challenge to solve the problem was already a herculean task, not giving in to mere random search (without modifications to randomness or bias) was more challenging.
- However, being pushed against a wall, we believe we have found a solution that is more time efficient because of the definitive and finite state-space. 

### Issues while continuing with solution and challenges :

- Can `A* search` be used when there is no goal state? -> yes, but since the heuristic is not going to be anything near-perfect,
it is no different from local-search or even just an iterative - DFS with large number of conditions to check.
	- What all meta_data needs to be maintained?
	- The Starting Problem - where do we start to take on this problem?
	- how do we read just the teams
	- heuristic -> how do we decide the heuristic function?
		- it wont matter if the cost is minimum overall
		- maximum time is added when there are more people who are assigned with dont-want-to-work-with
		- also, more the number of teams, more time.
	- local-search seems more promising an algorithm to continue on the task once the first set of teams are formed.
