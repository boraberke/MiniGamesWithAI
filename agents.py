import random
class Agent():
    def __init__(self,depth):
        self.depth_limit = depth
    
    def evaluation_function(self,game_state):
        return None

# this minimax algorithm was made for COMP 341 homework taken from CS 188 Pacman assignment of Berkeley.
# following is derived from my solutions.
class Minimax_Agent(Agent):

    def get_best_action(self,game_state,depth,agent_index):
        if(game_state.is_start_state()):
            return 0,random.choice(game_state.get_legal_actions())
        return self.value(game_state,depth,agent_index)
    # this method selects the next step to be calculated
    def value(self,game_state,depth, agent_index):
        if (depth==self.depth_limit or is_ended(game_state)): 
            return self.evaluation_function(game_state),""
        # if agent is max agent
        if (agent_index==1):
            return self.max_value(game_state,depth,agent_index)
        else:
            return self.min_value(game_state,depth,agent_index)
    #minimax max part
    def max_value(self,game_state,depth,agent_index):
        v = -9999999,""
        for action in game_state.get_legal_actions():
            successor = game_state.generate_successor_state(agent_index,action)
            next_agent=(agent_index+1)%2
            next_agent_depth = depth
            if next_agent-2==0:
                next_agent_depth=next_agent_depth+1
            value = max(v[0],self.value(successor,next_agent_depth,next_agent)[0])
            if (value!=v[0]):
                v=value,action  
        return v
    #minimax min part
    def min_value(self,game_state,depth,agent_index):
        v = 9999999,""
        for action in game_state.get_legal_actions():
            successor = game_state.generate_successor_state(agent_index,action)
            next_agent = (agent_index+1)
            next_agent_depth = depth
            if next_agent-2==0:
                next_agent_depth=next_agent_depth+1
                next_agent = 0
            value = min(v[0],self.value(successor,next_agent_depth,next_agent)[0])
            if (value!=v[0]):
                v=value,action  
        return v
    
    def evaluation_function(self,game_state):
        return game_state.check_end_game()[0].value

def is_ended(game_state):
    if (game_state.check_end_game()[0] == ''):
        return False
    else:
        return True
       