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
    Iterates through all states and sets the values to the respective rewards
    Then iterates through by the value of iters in order to choose the actions
    based on rewards and values multiplied by discountrate
    Lastly self.values is assigned the values given by newVals through use of a for loop
    """
    """ YOUR CODE HERE """
    for state in mdp.getStates():
      self.values[state] = mdp.getReward(state, 'Stop', state)
    for iter in range(1,iters):
      newVals = util.Counter()
      for state in mdp.getStates():
        tempVals = util.Counter()
        for action in mdp.getPossibleActions(state):
          for transStateProb in mdp.getTransitionStatesAndProbs(state, action):
            transState = transStateProb[0]
            transProb = transStateProb[1]
            tempVals[action] += transProb * (mdp.getReward(state, action, transState) + self.discountRate * self.values[transState])
          newVals[state] = tempVals[tempVals.argMax()]
      for state in mdp.getStates():
        self.values[state] = newVals[state]
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
    qVal is set to self.values in the given state
    A for loop is used in order to get reachable states and their probabilities
    through which we find our qValues

    """
    """ YOUR CODE HERE """
    qVal = self.values[state]
    for transStateProb in self.mdp.getTransitionStatesAndProbs(state, action):
      transState = transStateProb[0]
      transProb = transStateProb[1]
      qVal += transProb * (self.mdp.getReward(state, action, transState) + self.discountRate * self.values[transState])
    return qVal
    # """ END CODE """

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
    Initiates the best action at none
    Checks if there are available legal actions which if there are not will cause the
    bestAction to stay and be returned as None
    If there are legal actions available a loop iterates looking for the best action
    that can be taken and returns it by using argMax to return the action that has
    the highest QValue

    """
    """ YOUR CODE HERE """
    bestAction = None
    legalActions = self.mdp.getPossibleActions(state)
    if len(legalActions) > 0:
      tempVals = util.Counter()
      for action in legalActions:
        tempVals[action] = self.getQValue(state, action)
      bestAction = tempVals.argMax()
    return bestAction
    """ END CODE """

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
