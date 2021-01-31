import random
import util
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
        return None
    
class Minimax_Agent_TicTacToe(Minimax_Agent):
    def evaluation_function(self,game_state):
        return game_state.check_end_game()[0].value

def is_ended(game_state):
    if (game_state.check_end_game()[0] == ''):
        return False
    else:
        return True

class Approximate_QLearning_Agent():
    def __init__(self,feature_extractor,learning_rate=0.5,discount=0.9,epsilon=0.05):
        self.features = feature_extractor
        self.weights = self.initialize_weights()
        self.learning_rate = learning_rate
        self.discount = discount
        self.epsilon = epsilon
        self.episode_limit = 300
    
    def initialize_weights(self):
        #get feature keys
        keys = self.features.get_default_features().keys()
        # initialize all weights to 0.
        return dict.fromkeys(keys,0)

    def update(self,state,action):
        '''
        updates feature weights according to approximate q-learning algorithm.
        difference = ( (reward + discount * (max_a' Q(s',a'))) - Q(s,a))
        w_i <-- w_i + learning_rate * difference * f_i(s,a)
        '''
        new_weights = dict()
        next_state = state.next_state(action)
        
        reward = next_state.get_reward()
        for key,value in self.weights.items():
            old_weight = value
            # if terminal state
            if next_state.is_ended():
                max_next_state_action = 0.0
            else:
                max_next_state_action = max(self.get_q_value(next_state,action) for action in next_state.get_legal_actions())
            features = self.features.get_features(state,action)
            difference = reward + self.discount * max_next_state_action - self.get_q_value(state,action)
            new_weight = old_weight + self.learning_rate * difference * features[key]
            new_weights.update({key:new_weight})
        self.weights = new_weights
        return self.weights

    def get_q_value(self,state,action):
        '''
        return sum of dot product of weights and feature values.
        Q(s,a) = w_1 * f_1(s,a) + w_2 * f_2(s,a) + .... + w_n * f_n(s,a)
        '''
        features = self.features.get_features(state,action)
        return sum(features.get(k) * self.weights.get(k) for k in features.keys())
    def compute_action_from_q_values(self,state):
        '''
        computes the optimal action from q_values of a given state.
        '''
        legal_actions = state.get_legal_actions()
        q_values = dict()
        for action in legal_actions:
            q_values[action] = self.get_q_value(state,action)
        return max(q_values,key=q_values.get)
            
                
    def get_action(self,state):
        """
          Computes the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.
        """
        # Pick Action
        legal_actions = state.get_legal_actions()
        action = None
        # pick a random action with probability epsilon
        if (util.get_random_bool(self.epsilon)):
          action = random.choice(legal_actions)
        else:
          action = self.compute_action_from_q_values(state)
        return action

        

       