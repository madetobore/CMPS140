# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discountRate = 0.9, iters = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discountRate = discountRate
    self.iters = iters
    self.values = util.Counter() # A Counter is a dict with default 0

    """Description:
    [Enter a description of what you did here.]
    """
    """ YOUR CODE HERE """
    for iter in range(0, iters):
      for state in mdp.getStates():
        maxUtil = 0
        maxReward = 0
        for action in mdp.getPossibleActions(state):
          tempUtil = 0
          for temp in mdp.getTransitionStatesAndProbs(state, action):
            nextState = temp[0]
            nextProb = temp[1]
            nextReward = mdp.getReward(state, action, nextState)
            tempUtil += nextProb * self.values[nextState]
          if tempUtil >= maxUtil:
            maxUtil = tempUtil
            maxReward = nextReward
        self.values[state] = maxReward + maxUtil * discountRate


    #util.raiseNotDefined()

    """ END CODE """

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]

    # """Description:
    # [Enter a description of what you did here.]
    # """
    # """ YOUR CODE HERE """
    # util.raiseNotDefined()
    # """ END CODE """

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    """Description:
    [Enter a description of what you did here.]
    Based on Q-learning from Sutton
    transState is used to be the current state with transProb being the
    possible next state
    possQ is the value associated with the transProb state
    If the value of possQ is greater than that of the maxQ, maxQ is then
    replaced

    """
    """ YOUR CODE HERE """
    maxQ = 0;
    for transition in self.mdp.getTransitionStatesAndProbs(state, action):
        transState = transition[0]
        transProb = transition[1]
        possQ = transProb * self.values[transState]
        if possQ >= maxQ:
          maxQ = possQ
    return maxQ
    # util.raiseNotDefined()
    """ END CODE """

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """

    """Description:
    [Enter a description of what you did here.]
    Initialize bestAction to an empty string to be filled with a movement
    The for loop goes through the possible actions in order to find the move
    that would in theory be the best in regards to the policy, by going through
    the actions, the highest q value is set as maxVal in order to select the
    best action that is returned
    """
    """ YOUR CODE HERE """
    if not self.mdp.getPossibleActions(state):
       return None

    bestAction = ""
    maxVal = 0
    for action in self.mdp.getPossibleActions(state):
      tempReward = self.getQValue(state, action)
      if tempReward > maxVal:
        maxVal = tempReward
        bestAction = action
    return bestAction

    # util.raiseNotDefined()
    """ END CODE """

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
