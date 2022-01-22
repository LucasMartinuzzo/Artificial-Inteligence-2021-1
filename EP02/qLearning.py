# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 11:02:20 2021

@author: Lucas Martinuzzo Batista
@nusp: 11930158
"""
import numpy as np
#Configuration to print the number in a organized way
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
#Set seed so the experiments are repeatable
np.random.seed(1)

#Number of maximum episodes the algorithm will run before stops.
MAX_EPISODES = 1000
#Number of maximum iterations each episode will have. One iteration is equivalent
#to make one action.
MAX_ITERATIONS_PER_EPISODE = 1000
#If the algorithm makes this number of sequential episodes and get the same 
#results, it stops.
MAX_EPISODES_WITHOUT_CHANGE = 5
#Probability of the algorithm take a different action of the intended one.
CHANGE_RANDOM_STATE = 0.10

class Action:
    """
    Class to organize the possible actions
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    ALL = [UP,RIGHT,DOWN,LEFT]
    ALL_STRING = ["UP","RIGHT","DOWN","LEFT"]


class State:
    """
    This class manages a state. A state is a position on the board and all
    information relate to it.
    """
    def __init__(self, reward,index,close_indexes,final_state = False):
        self.reward = reward
        self.visits = [0,0,0,0]
        self.qualities = [.0,.0,.0,.0]
        self.final_state = final_state
        if(final_state):
            self.qualities = [reward,reward,reward,reward]
        self.close_indexes = close_indexes
        self.index = index
        
    
    def alfa(self,N):
        if N == 0:
            return 1.0
        return 1.0/N

    def updateVisit(self, action):
        self.visits[action]+=1.0
        
    
    def getQualities(self):
        return self.qualities
    
    def getQualityAction(self,action):
        return self.qualities[action]
    
    def getVisits(self):
        return self.visits
    
    def getVisitAction(self,action):
        return self.visits[action]
    
    def getReward(self):
        return self.reward
    
    def setReward(self,reward):
        self.reward = reward
        
    def isFinalState(self):
        return self.final_state
    
    """
    Set a Final state. By definition final states have their qualities set equal
    to their rewards.
    """
    def setFinalState(self):
        self.final_state = True
        self.qualities = [self.reward,self.reward,self.reward,self.reward]
        
    def getCloseIndexes(self):
        return self.close_indexes
    
    def getIndex(self):
        return self.index

    def getNextStateIndex(self,action):
        index = self.getCloseIndexes()[action]
        return index
    
    """
    Calculate the exploratory rate. If number of visits = 0, returns 1.
    If not, return Quality*Number of Visit. The product is done because 
    the rewards are negatives, so the qualities tend to be negative. This way,
    the more the action is made, more negative is the quality of that action and
    less times it will be selected.
    This function calculates the rate for all actions of the state.
    """
    def exploratoryRates(self):
        rates = []
        for action in Action.ALL:
            if self.getVisitAction(action) == 0:
                rates.append(1)
            elif  self.getQualityAction(action) > 0:
                rates.append(self.getQualityAction(action)/self.getVisitAction(action))
            else:
                rates.append(self.getQualityAction(action)*self.getVisitAction(action))
        return rates
    
    
    """
    update the Quality with the formula
    quality += alfa*(reward + gamma*max(qualities') - quality)
    where qualities' are the qualities of the next states for all possible
    actions
    """
    def updateQuality(self,action,max_quality,gamma):
        n_visits = self.getVisitAction(action)
        alfa = self.alfa(n_visits)
        reward = self.getReward()
        current_quality = self.getQualityAction(action)
        new_quality = current_quality + alfa*(reward + gamma*max_quality - current_quality)
        self.qualities[action] = new_quality
        return new_quality
    

class Board:
    """
    This class manages the board and the movement through it.
    It create states for each space on the board and set their configurations.
    Also 
    """
    
    """
    Set adjacent states of an state based on the board.
    It considers that an movement to a wall results in staying on the current state.
    """
    @staticmethod
    def calculateCloseIndexes(shape,state_row,state_column):
        up_state = (state_row,state_column)
        if(state_row > 0):
            up_state = (state_row - 1, state_column)
            
        down_state = (state_row,state_column)
        if(state_row < shape[0] - 1):
            down_state = (state_row + 1, state_column)
            
        left_state = (state_row,state_column)
        if(state_column > 0):
            left_state = (state_row, state_column - 1)
            
        right_state = (state_row,state_column)
        if(state_column < shape[1] - 1):
            right_state = (state_row, state_column + 1)
        
        return [up_state,right_state,down_state,left_state]
    
    

    def __init__(self,shape,initial_index,default_reward,gamma,final_state_list,special_rewards_dict):
        self.board = np.ndarray(shape,dtype=np.object)
        for i in range(shape[0]):
            for j in range(shape[1]):
                close_indexes = self.calculateCloseIndexes(shape,i,j)
                index = (i,j)
                self.board[i,j] = State(default_reward,index,close_indexes)
                
        self.initial_index = initial_index
        
        self.current_index = initial_index
        
        self.shape = shape
        
        self.gamma = gamma
        
        for state,reward in special_rewards_dict.items():
            self.board[state].setReward(reward)
       
        for state in final_state_list:
            self.board[state].setFinalState()
        
        self.current_state = self.board[initial_index]
    
    def getShape(self):
        return self.shape
    
    def getCurrentState(self):
        return self.current_state
    
    def changeCurrentState(self,state):
        self.current_index = state.getIndex()
        self.current_state = state
        
    def getBoard(self):
        return self.board
    
    def getState(self,index):
        return self.board[index]

    """
    Get all the states adjacent to the corrent one.
    """
    def getCurrentCloseStates(self):
        indexes = self.getCurrentState().getCloseIndexes()
        return np.array([self.getState(index) for index in indexes])
    
    """
    Calculate the next action based on the exploratory rates of the current state.
    If more than one action have the same exploratory rate, a random action
    is selected.
    """
    def calculateNextAction(self):
        values = np.array(self.getCurrentState().exploratoryRates())
        largest_indexes = np.argwhere(values == np.max(values)).flatten()
        action = Action.ALL[np.random.choice(largest_indexes)]
        return action
    
    """
    Given an action, get the state resulted from doing that action in the current
    state.
    """
    def getNextState(self,action):
        next_state_index = self.getCurrentState().getNextStateIndex(action)
        return self.getState(next_state_index)
    
    
    """The following methods are getter that helps the algorithm work or be
    debugged.
    """
    def getRewards(self):
        return np.array([[self.getState((i,j)).getReward() for j in range(self.getShape()[1])] for i in range(self.getShape()[0])])
    
    def getQualities(self,states = None):
        if states is None:
            return np.array([[self.getState((i,j)).getQualities() for j in range(self.getShape()[1])] for i in range(self.getShape()[0])])
        else:
            return np.array([state.getQualities() for state in states])
    
    def getMaxQualities(self):
        return np.array([[np.max(self.getState((i,j)).getQualities()) for j in range(self.getShape()[1])] for i in range(self.getShape()[0])])
    
    def getQualitiesAction(self,action):
        return np.array([[self.getState((i,j)).getQualityAction(action) for j in range(self.getShape()[1])] for i in range(self.getShape()[0])])
    
    def getMaxActions(self):
        return np.array([[Action.ALL_STRING[np.argmax(self.getState((i,j)).getQualities())] for j in range(self.getShape()[1])] for i in range(self.getShape()[0])])
    
    def getVisits(self):
        return np.array([[self.getState((i,j)).getVisits() for j in range(self.getShape()[1])] for i in range(self.getShape()[0])])
    
    def getFinalStates(self):
        return np.array([[self.getState((i,j)).isFinalState() for j in range(self.getShape()[1])] for i in range(self.getShape()[0])])
    

def main():
    #Configurations based on the board passed on exercise 1
    shape = (3,4)
    initial_index = (2,0)
    default_reward = - 1.0
    gamma = 1.0
    final_state_indexes = [(0,3)]
    special_rewards = {(0,3): 100.0,
                       (1,1): -100.0}
    
    #Rewards based on exercise 2
    special_rewards2 = {(2,3): 10.0,
                       (1,1): -100.0,
                       (0,3): 100.0}
    #Select which exercise it will run. It helps reutilize code.
    while(True):
        exercise = input("Which exercise do you want to run? (1/2): ")
        if exercise == '1' or exercise == '2':
            break;
    if exercise == '1':
        board = Board(shape,initial_index,default_reward,gamma,final_state_indexes,special_rewards)
    else:
        board = Board(shape,initial_index,default_reward,gamma,final_state_indexes,special_rewards2)
    
    
    initial_state = board.getCurrentState()
    final_states = board.getFinalStates()
    movements = []
    states_walked = [initial_index]
    episodes_without_change = 0
    
    for episode in range(MAX_EPISODES):
        #Set the robot to the initial state
        board.changeCurrentState(initial_state)
        new_movements = []
        states_walking = [initial_state.getIndex()]
        #print("Episode Iniciated:",episode)
        for iteration in range(MAX_ITERATIONS_PER_EPISODE):
            #Calculates the best action
            calculated_action = board.calculateNextAction()
            real_action = calculated_action
            #There is 10% chance the algorithm chooses one states but goes to another.
            #The CHANGE_RANDOM_STATE is multiplied by 4/3 because even if the random
            #probability is under 10% there is still 1/4 it chooses the same action
            #so the probability to change actions is 0,10*(4/3)*(3/4) = 0,10 as choosed
            if(np.random.sample() <= 4.0*CHANGE_RANDOM_STATE/3.0):
                real_action = np.random.choice(Action.ALL)
            #action_str = Action.ALL_STRING[calculated_action]
            #print(action_str)
            real_action_str = Action.ALL_STRING[real_action]
            new_movements.append(real_action_str)
            next_state = board.getNextState(real_action)
            current_state_index = board.getCurrentState().getIndex()
            next_state_index = next_state.getIndex()
            states_walking.append(next_state_index)
            #print(current_state_index," -> ",next_state_index)
            qualities = next_state.getQualities()
            max_quality = np.max(qualities)
            #Even if it makes a different action of the intended one.
            #The visit counter and the quality of the latter must be updated.
            board.getCurrentState().updateVisit(calculated_action)
            board.getCurrentState().updateQuality(calculated_action,max_quality,gamma)
            #After all computation is made, the current state is updated.
            board.changeCurrentState(next_state)
            if(board.getCurrentState().isFinalState()):
                #print("Episode finished")
                break
        #Checks if the movements of the last iteration and the one before it
        # were equal.
        if(movements == new_movements):
            episodes_without_change+=1
        else:
            episodes_without_change = 0
        movements = new_movements
        states_walked = states_walking
        #print("number of movements:",len(movements))
        #print("movements:\n",movements)
        #print("states walked:\n",states_walked)
        #print("last calculated_action",action_str)
        
        if(episodes_without_change == MAX_EPISODES_WITHOUT_CHANGE):
            break
    print("\nAlgorithm finished after {} episodes\n".format(episode+1))
    print("Actions after algorithm converged/finished:\n",movements)
    print("\nStates walked on last iteration:\n",states_walked)
    #rewards = board.getRewards()
    #print('rewards:\n',rewards)
    qualities = board.getMaxQualities()
    print('\nMaximum qualities obtained:\n',qualities)
    actions = board.getMaxActions()
    print('\nActions corresponding to qualities above:\n',actions)
    qualities_up = board.getQualitiesAction(Action.UP)
    print('\n Qualities obtained for action UP:\n',qualities_up)
    qualities_right = board.getQualitiesAction(Action.RIGHT)
    print('\n Qualities obtained for action RIGHT:\n',qualities_right)
    qualities_down = board.getQualitiesAction(Action.DOWN)
    print('\n Qualities obtained for action DOWN:\n',qualities_down)
    qualities_left = board.getQualitiesAction(Action.LEFT)
    print('\n Qualities obtained for action LEFT:\n',qualities_left)
    return 0

main()