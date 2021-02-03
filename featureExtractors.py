import util
class FeatureExtractor:
    
    @staticmethod
    def get_features(state,action):
        '''
        returns a dictionary of feature-value pairs given state,action.
        '''
        return None
    @staticmethod
    def get_default_features():
        '''
        returns default values for the features.
        '''

class SnakeSimpleExtractor(FeatureExtractor):

    @staticmethod
    def get_features(state,action):
        features = dict()
        # get the s'(next state) state to make calculations 
        next_state = state.next_state(action)
        food = state.get_food()
        snake_head = next_state.get_snake_head()
        distance_to_food =  util.manhattan_distance(snake_head,food)
        # make distance_to_food between 0 and 1 so that it will not diverge with every update.
        distance_to_food = float(distance_to_food) / (next_state.height*next_state.width)
        features['distance_to_food'] = distance_to_food
        # 1 step away means that only the points that snake can move after one step. 
        # Therefore, it doesn't include diagonals and back of the snake as it cannot move there
        from snake import Squares
        #features['#_of_walls_1_step_away'] = get_adjacent_count(next_state,Squares.Wall)
        tunnel_count,count = get_dead_end_count(next_state,Squares.Snake,Squares.Wall)
        features['dead_end'] = 1 if tunnel_count==2 or count==3 else 0
        features['is_end_game'] = 1 if next_state.check_end_game() else 0
        util.divide_all(features,100.0)
        return features
        
    @staticmethod
    def get_default_features():
        features = dict()
        features['distance_to_food'] = 1
        #features['#_of_walls_1_step_away'] = 1
        features['dead_end'] = 0
        features['is_end_game'] = 0
        return features

def get_dead_end_count(state,square1,square2):
    '''
    return tunnel_count,count of "squares" that may cause to enter a dead end.
    '''
    positions = state.get_adjacent_positions()
    count = 0
    tunnel_count = 0
    # way is either front or side, helping to detect tunnels/ dead ends
    for way,positions in positions.items():
        for pos in positions:
            if (state.get_pos(pos).value==square1.value or state.get_pos(pos).value == square2.value):
                count += 1
                if(way =='side'):
                    tunnel_count+=1
    return tunnel_count,count

