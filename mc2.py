''' mclib.py '''

#Here is where I define my state. I am initalising my program

class MCState:
    ### MC is missionaries and cannibals
    def __init__(self, state_vars_change_change, num_moves=0, parent=None):
        self.state_vars_change_change = state_vars_change_change
        self.num_moves = num_moves
        self.parent = parent

 
    @classmethod
    def root(cls):
        return cls((3,3,1))

#setting up the ampount of moves that I can take 
    def getPossibleMoves(self):
        # looking to see how I can move the cannoblist or missionaries

        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        return moves
    
    def ifLegal(self):
        missionaries = self.state_vars_change_change[0]
        cannibals = self.state_vars_change_change[1]
        ## is checking to see how may of each group is stuck on each side 
         
        if missionaries < 0 or missionaries > 3: 
            return False
        elif cannibals < 0 or cannibals > 3:
            return False
        return True
    
        ##getting my possible soultion of having everyone on the other side 
    
    def iFsolution(self):
        if self.state_vars_change == (0,0,0):
            return True
        return False
    
    #
    def iFfailure(self):
        missionaries = self.state_vars_change[0]
        cannibals = self.state_vars_change[1]
        boat = self.state_vars_change[2]
        # This shows what would happen if I dont get the right pattern  
        
        ### missionaries on right side AND more cannibals than missionaries
        if missionaries > 0 and missionaries < cannibals:
            return True
        
        # this is me tring to move the missionaries over  
        missionaries_on_left = 3 - missionaries
        cannibals_on_left = 3 - cannibals
        if missionaries_on_left > 0 and missionaries_on_left < cannibals_on_left:
            return True
        ## if you replace the math in, you get:
        #i
        return False
        

    def get_possible_moves(self):
        ##this is used to help move from point a to b 

        moves = self.get_possible_moves()
        all_states = list()
        mis_right, can_right, raft_right = self.state_vars_change_change
        ## if raft is on right, subtract move from these numbers
        ## if raft is on left, add these move numbers to these numbers
        for move in moves:
            change_mis, change_can = move
            if raft_right == 1:  ## mis_right = 3; can_right = 3, raft_right = 1
                new_state_vars_change = (mis_right-change_mis, can_right-change_can, 0)
            else:
                new_state_vars_change = (mis_right+change_mis, can_right+change_can, 1)
            
            ## notice the number of moves is increasing by 1
            ## also notice we are passing self to our child.
            new_state = MCState(new_state_vars_change, self.num_moves+1, self)
            if new_state.is_legal():
                all_states.append(new_state)

        return all_states

    def __str__(self):
        return "MCState[{}]".format(self.state_vars_change)

    def __repr__(self):
        return str(self)


def search(dfs=True):
    
    
    ### tstarting my queue here 
    from collections import deque
    
    ### create the root state
    root = MCState.root()
        
        
    ### we use the stack/queue for keeping track of where to search next
    to_search = deque()
    
    #
    seen_states = set()
    
    ### use a list to keep track of the solutions that have been seen and we dont need 
    solutions = list()
    
    ### start the search with the root
    to_search.append(root)
    
   
    loop_count = 0
    max_loop_total = 10000
    
    #beging my list 
    all_depths = []
    
    ### while the stack/queue still has items
    while len(to_search) > 0:
        loop_count += 1
        if loop_count > max_loop_total:
            print(len(to_search))
            break
    
        ### get the next item
        current_state = to_search.pop()
        
       
        ## this uses the rule for actions and moves to create next states
      
        next_states = current_state.get_possible_moves()
        
        ## next_states is a list, so iterate through it
        for possible_next_state in next_states[::-1]:
            
            ## to see if we've been here before, we look at the state variables
            possible_state_vars_change = possible_next_state.state_vars_change
            
            ## we use the set and the "not in" boolean comparison 
            if possible_state_vars_change not in seen_states:
                all_depths.append(possible_next_state.num_moves)
                
                if possible_next_state.is_failure():
                    #print("Failure!")
                    continue
                elif possible_next_state.is_solution():
                    ## Save it into our solutions list 
                    solutions.append((possible_next_state, len(all_depths)-1))
                    #print("Solution!")
                    continue
                    
               
                   
           
                
               
              
                if dfs:
                    to_search.append(possible_next_state)
                else:
                    to_search.appendleft(possible_next_state)

                
                seen_states.add(possible_state_vars_change)
                
    ## finally, we reach this line when the stack/queue is empty (len(to_searching==))
    print("Found {} solutions".format(len(solutions)))
    return solutions, all_depths

sol_dfs, depths_dfs = search(True)
sol_bfs, depths_bfs = search(False)

plt.figure(figsize=(10,2))
plt.plot(depths_dfs, label='depth first search')
for _, idx in sol_dfs:
    plt.scatter(idx, depths_dfs[idx], marker='x', alpha=0.8, s=100)
plt.plot(depths_bfs, label='breadth first search', color='green')
for _, idx in sol_bfs:
    plt.scatter(idx, depths_bfs[idx], marker='o', alpha=0.5, s=80, color='green')
plt.legend(loc=2, frameon=False)
plt.xlabel("Order of Actions Explore")
plt.ylabel("Depth")
plt.xlim(0,35)

current_state = sol_dfs[0][0]
while current_state:
    print(current_state)
    current_state = current_state.parent
    
print("--")
current_state = sol_dfs[1][0]
while current_state:
    print(current_state)
    current_state = current_state.parent