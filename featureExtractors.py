from queue import Queue

import util


class FeatureExtractor:

    @staticmethod
    def get_features(state, action):
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
    def get_features(state, action):
        features = dict()
        # get the s'(next state) state to make calculations 
        next_state = state.next_state(action)
        food = state.get_food()
        snake_head = next_state.get_snake_head()
        distance_to_food = util.manhattan_distance(snake_head, food)
        # make distance_to_food between 0 and 1 so that it will not diverge with every update.
        distance_to_food = float(distance_to_food) / (next_state.height * next_state.width)
        features['distance_to_food'] = distance_to_food
        # 1 step away means that only the points that snake can move after one step. 
        # Therefore, it doesn't include diagonals and back of the snake as it cannot move there
        from snake import Squares
        # features['#_of_walls_1_step_away'] = get_adjacent_count(next_state,Squares.Wall)
        tunnel_count, count = get_dead_end_count(next_state, Squares.Snake, Squares.Wall)
        # features['dead_end'] = 1 if tunnel_count == 2 or count == 3 else 0
        depth = 6
        features['new_dead_end'] = 1 if is_dead_end(state, action, depth) else 0
        features['is_end_game'] = 1 if next_state.check_end_game() else 0
        util.divide_all(features, 100.0)
        return features

    @staticmethod
    def get_default_features():
        features = dict()
        features['distance_to_food'] = 1
        # features['#_of_walls_1_step_away'] = 1
        # features['dead_end'] = 0
        features['new_dead_end'] = 0
        features['is_end_game'] = 0
        return features


def get_dead_end_count(state, square1, square2):
    '''
    return tunnel_count,count of "squares" that may cause to enter a dead end.
    '''
    positions = state.get_adjacent_positions()
    count = 0
    tunnel_count = 0
    # way is either front or side, helping to detect tunnels/ dead ends
    for way, positions in positions.items():
        for pos in positions:
            if state.get_pos(pos).value == square1.value or state.get_pos(pos).value == square2.value:
                count += 1
                if way == 'side':
                    tunnel_count += 1
    return tunnel_count, count


def is_dead_end(state, action, depth):
    '''
    Checks whether a given state and action will go to a dead end until 'depth' times iteration.
    :param state:  current state to check.
    :param action: action to take in the state.
    :param depth: depth limit. It will test until depth.
    :return: returns True if state,action will cause going to a dead end, False otherwise.
    '''
    expanded_states = []
    s_a_pairs = Queue()
    s_a_pairs.put((state, [action]))
    expanded_states.append(state)
    for _ in range(depth):
        state, actions = s_a_pairs.get()
        while state in expanded_states:
            if not s_a_pairs.empty():
                state, actions = s_a_pairs.get()
            else:
                break
        for i in range(len(actions)):
            # update state by taking the state
            action = actions[i]
            next_state = state.next_state(action)
            expanded_states.append(next_state)
            # if the state is end state and there are no alternative actions to take, then it is a dead end.
            if next_state.check_end_game():
                if s_a_pairs.empty() and i == len(actions) - 1:
                    return True
            else:
                legal_actions = next_state.get_legal_actions()
                s_a_pairs.put((next_state, legal_actions))
    return False


