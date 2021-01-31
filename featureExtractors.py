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
        features['#_of_snake_1_step_away'] = get_adjacent_count(next_state,Squares.Snake)
        features['is_end_game'] = 1 if next_state.check_end_game() else 0
        util.divide_all(features,10.0)
        return features
        
    @staticmethod
    def get_default_features():
        features = dict()
        features['distance_to_food'] = 1
        #features['#_of_walls_1_step_away'] = 1
        features['#_of_snake_1_step_away'] = 1
        features['is_end_game'] = 0
        return features

def get_adjacent_count(state,square):
    '''
    return number of "square" in adjacent squares.
    '''
    positions = state.get_adjacent_positions()
    count = 0
    for pos in positions:
        if (state.get_pos(pos).value==square.value):
            count += 1
    return count

