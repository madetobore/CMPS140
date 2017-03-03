# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discountRate (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)
    self.qValues = util.Counter() #similar to values in valueIterationAgents.py


  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    """Description:
    [Enter a description of what you did here.]
    If there was no qValue return 0.0 as indicated otherwise
    return the tuple
    """
    """ YOUR CODE HERE """
    if (state, action) not in self.qValues:
      return 0.0
    else:
      return self.qValues[(state, action)]
    # util.raiseNotDefined()
    # """ END CODE """



  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    """Description:
    [Enter a description of what you did here.]
    Check first if legal action is available if not return 0.0
    Otherwise iterates through actions to find the next action
    and then returns it
    """
    """ YOUR CODE HERE """
    # if legalActions[0] == "exit":
    if self.getLegalActions(state)[0] == "exit":
      return 0.0
    else:
      max_action = -float("infinity")
      for nextAction in self.getLegalActions(state):
        if max_action <= self.getQValue(state, nextAction):
          max_action = self.getQValue(state, nextAction)
      return max_action
    # util.raiseNotDefined()
    # """ END CODE """

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    """Description:
    [Enter a description of what you did here.]
    Similar to getPolicy from valueIteration agents in how it checks for available actions
    Goes through a loop to find the best actions and puts them in a list in order
    to reference them later to find the bestaction
    """
    """ YOUR CODE HERE """
    # if not self.getLegalActions(state):
    # if self.getLegalActions(state)[0] == "exit":
    #   return None
    bestAction = None
    maxQVal = 0
    bestActions = []
    if (len(self.getLegalActions(state)) > 0):
      # maxQVal = 0
      for action in self.getLegalActions(state):
        if maxQVal <= self.getQValue(state, action):
          maxQVal = self.getQValue(state, action)
          bestAction = action
          bestActions.append(bestAction)
      # return bestAction

    # bestActions = []
    for action in self.getLegalActions(state):
      if maxQVal == self.getQValue(state, action):
        bestActions.append(action)
    bestAction = random.choice(bestActions)
    return bestAction
    # util.raiseNotDefined()
    """ END CODE """

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    legalActions = self.getLegalActions(state)
    action = None

    """Description:
    [Enter a description of what you did here.]
    If there are no legal actions return none
    Uses flipCoin to return whether to choose a random action or use what the policy
    returns

    """
    """ YOUR CODE HERE """
    if len(legalActions) < 1:
      return None

    else:
      randomAction = util.flipCoin(self.epsilon)

      if randomAction:
        action = random.choice(legalActions)
      else:
        action = self.getPolicy(state)

      return action
    # util.raiseNotDefined()
    # """ END CODE """

    # return action

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    """Description:
    [Enter a description of what you did here.]
    Finds qvalues and then returns the action associated with the next state if not
    terminal
    """
    """ YOUR CODE HERE """
    legalActions = self.getLegalActions(state)

    if legalActions[0] == "exit":
    # if legalActions < 1:
      self.qValues[(state, action)] = reward
    else:
      self.qValues[(state, action)] = self.getQValue(state, action) + self.alpha * (reward + self.discountRate * self.getValue(nextState) - self.getQValue(state, action))
    action = self.getAction(nextState)
    return action
    # util.raiseNotDefined()
    """ END CODE """

class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)

    # You might want to initialize weights here.

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    """Description:
    [Enter a description of what you did here.]
    """
    """ YOUR CODE HERE """
    util.raiseNotDefined()
    """ END CODE """

  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    """Description:
    [Enter a description of what you did here.]
    """
    """ YOUR CODE HERE """
    util.raiseNotDefined()
    """ END CODE """

  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      util.raiseNotDefined()
