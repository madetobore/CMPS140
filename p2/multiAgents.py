# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPosition = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] #tried finding reason to use this but was not able to find good way for pacman to go after scared ghosts

    "*** YOUR CODE HERE ***"
    #Minimum required elements needed seem to have been position/number of food, ghosts and capsules relative to
    #pacman
    #Tried to have scared ghosts seem equivalent if not more of a reward than food but ended up having pacman just go
    #for food instead
    #Values used simply numbers divisible by 5 for the most part

    # print successorGameState
    # print  newGhostStates

    #code snippet of how to use getfood() for positions
    # currentFood = state.getFood()
    # if currentFood[x][y] == True: ...

    foodSpots = oldFood.asList() #working with food as list is easier for location checking, function found in game.py grid Class
    score = currentGameState.getScore() #to avoid using getScore multiple times later

    #Needed in order to have a goal state, seems to work without isWin() but left that in case any strange
    #outcomes were to occur
    if successorGameState.isWin():
      return float("inf")
    if successorGameState.isLose():
      return -float("inf")

    ghostPos = currentGameState.getGhostPosition(1)
    pacGhostDist = 1/max(util.manhattanDistance(newPosition, ghostPos), 1) #uses max comparing with 1 so as to not crash for having 0 in denominator
    # print util.manhattanDistance(newPosition, ghostPos)
    if newScaredTimes >= 0:
      scaredPacGhostDist = util.manhattanDistance(newPosition, ghostPos)
      score += 1/max(scaredPacGhostDist, 1) # reciprocal may help later
    else:
      score += pacGhostDist
      # score += max(pacGhostDist,3) #reciprocal may help later
      # score -= (max(pacGhostDist, 5)*3 + successorGameState.getScore())


    nearbyFood = 50
    for foodSpot in foodSpots: #iterates through food location to find ideal food to go to next
       pacFoodDist = util.manhattanDistance(newPosition, foodSpot)
       if pacFoodDist < nearbyFood:
         nearbyFood = pacFoodDist
    #   # oldFood = currentGameState.getFood()

    #this section compares the amount of food in order to give pacman the incentive of moving towards the food
    currentFoodNum = currentGameState.getNumFood()
    successorFoodNum = successorGameState.getNumFood()
    if currentFoodNum > successorFoodNum:
      score += 50

    score -= nearbyFood * 5 # incentive for pacman to not sit around

    score += max(pacGhostDist, 5)  # reciprocal may help later

    if action == Directions.STOP: #gives pacman incentive to move instead of staying stuck in one spot for long amounts of time
      score -= 10

    #gives incentive for pacman to move toward capsule while still comparing rewards for instead going towards the food
    #still a bit confused as to why pacman seems to always go for the food and never take the capsule, assuming it's
    # because i wasn't able to give enough incentive for chasing ghost after capsule
    capsuleList = currentGameState.getCapsules()
    # numCapsules = len(capsuleList)
    if successorGameState.getPacmanPosition() in capsuleList:
      score += 100
    #   pacCapsuleDist = util.manhattanDistance(capsuleList[0], newPosition)
    #   # score += pacCapsuleDist*5 + successorGameState.getScore()
    #   score += 100

    # print capsuleList
    # print oldFood
    # print ghostPos
    # print newPosition
    # return successorGameState.getScore()
    return score

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.treeDepth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.treeDepth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """

    #pseudocode from slides for easier reference while working
    # def value(state):
    # If the state is a terminal state: return the state's utility
    # If the next agent is MAX: return max-value(state)
    # If the next agent is MIN: return min-value(state)
    #
    # def max-value(state) :
    # Initialize max = -inf For each successor of state:
    # Compute value(successor)
    # Update max accordingly
    # Return max
    "*** YOUR CODE HERE ***"

    # ghosts, agentIndex used for the loop to keep track of each one's moves
    def minValue(gameState, treeDepth, ghostNum, agentIndex):
      # added treeDepth == 0 as termination to stop attempting to reach nonexistant index, isWin/isLose basic terminations
      if gameState.isWin() or gameState.isLose() or treeDepth == 0:
        return self.evaluationFunction(gameState)
      minVal = float("inf") #allows comparison to always pick the min
      ghostMoves = gameState.getLegalActions(agentIndex)
      if agentIndex == ghostNum: #different action if the last ghost
        for move in ghostMoves:
          #once last ghost is reached calls maxValue for pacman's next move
          minVal = min(minVal, maxValue(gameState.generateSuccessor(agentIndex, move), treeDepth-1,ghostNum))
      else:
        #recursive function in order to find all ghost moves, stays in same depth while index increases
        for move in ghostMoves:
          minVal = min(minVal, minValue(gameState.generateSuccessor(agentIndex, move), treeDepth, ghostNum, agentIndex + 1))


      return minVal

    def maxValue(gameState, treeDepth, ghostNum): #pacman
      # added treeDepth == 0 as termination to stop attempting to reach nonexistant index, isWin/isLose basic terminations
      if gameState.isWin() or gameState.isLose() or treeDepth == 0:
        return self.evaluationFunction(gameState)
      pacActions = gameState.getLegalActions(0) #gets pacmans actions
      maxVal = -float("inf") #initiates at this value to allow comparison to actually pick the max
      for moveChoice in pacActions:
        #generateSuccessor uses pacman's next move
        # minVal uses the successor, depth, number of ghosts, and 1 to reference that in the agent list ghosts are >= 1
        maxVal = max(maxVal, minValue(gameState.generateSuccessor(0, moveChoice),treeDepth-1, ghostNum, 1))
      return maxVal

    moves = gameState.getLegalActions()
    ghostNum = gameState.getNumAgents() - 1 #since pacman is index 0 this gives ghost number
    maxChoice = Directions.STOP #initiate on always legal state since basically neutral
    newScore = -float("inf")  # ensures first score chooses the max between score and what minvalue returns
    for nextMove in moves: #loop iniates to choose which actions to take
      nextState = gameState.generateSuccessor(0, nextMove)
      score = newScore
      newScore = max(score, minValue(nextState, self.treeDepth, ghostNum, 1))#finds minMove based off pacman's first move and self.treedepth
      if newScore > score:
        maxChoice = nextMove

    return maxChoice

    util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.treeDepth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    #replaced ghostNum with alpha/beta in order to go through the pruning process correctly
    # ghosts, agentIndex used for the loop to keep track of each one's moves
    def minValue(gameState, treeDepth, agentIndex, alpha, beta):
      # added treeDepth == 0 as termination to stop attempting to reach nonexistant index, isWin/isLose basic terminations
      if gameState.isWin() or gameState.isLose() or treeDepth == 0:
        return self.evaluationFunction(gameState)
      minVal = float("inf")  # allows comparison to always pick the min
      ghostMoves = gameState.getLegalActions(agentIndex)

      if agentIndex == ghostNum:  # different action if the last ghost
        for move in ghostMoves:
          # once last ghost is reached calls maxValue for pacman's next move
          minVal = min(minVal, maxValue(gameState.generateSuccessor(agentIndex, move), treeDepth - 1, alpha, beta))
          if minVal <= alpha:
            return minVal
          beta = min(beta, minVal)

      else:
        # recursive function in order to find all ghost moves, stays in same depth while index increases
        for move in ghostMoves:
          minVal = min(minVal,minValue(gameState.generateSuccessor(agentIndex, move), treeDepth, agentIndex + 1, alpha, beta))
          if minVal <= alpha:
            return minVal
          beta = min(beta, minVal)
      return minVal

    def maxValue(gameState, treeDepth, alpha, beta):  # pacman
      # added treeDepth == 0 as termination to stop attempting to reach nonexistant index, isWin/isLose basic terminations
      if gameState.isWin() or gameState.isLose() or treeDepth == 0:
        return self.evaluationFunction(gameState)
      pacActions = gameState.getLegalActions(0)  # gets pacmans actions
      maxVal = -float("inf")  # initiates at this value to allow comparison to actually pick the max
      for moveChoice in pacActions:
        # generateSuccessor uses pacman's next move
        # minVal uses the successor, depth, and 1 to reference that in the agent list ghosts are >= 1,
        # and alpha/beta for pruning
        maxVal = max(maxVal, minValue(gameState.generateSuccessor(0, moveChoice), treeDepth - 1, 1, alpha, beta))
        if maxVal >= beta:
          return maxVal
        alpha = max(alpha, maxVal)
      return maxVal

    #alpha and beta values necessary for alpha-beta pruning
    alpha = -float("inf")
    beta = float("inf")
    moves = gameState.getLegalActions()
    ghostNum = gameState.getNumAgents() - 1  # since pacman is index 0 this gives ghost number
    maxChoice = Directions.STOP  # initiate on always legal state since basically neutral
    newScore = -float("inf")  # ensures first score chooses the max between score and what minvalue returns
    for nextMove in moves:  # loop iniates to choose which actions to take
      nextState = gameState.generateSuccessor(0, nextMove)
      score = newScore
      newScore = max(score, minValue(nextState, self.treeDepth,1, alpha, beta))  # finds minMove based off pacman's first move and self.treedepth
      if newScore > score:
        maxChoice = nextMove

      if newScore >= beta:
        return maxChoice
      alpha = max(alpha, newScore)

    return maxChoice
    util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.treeDepth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"

    # def value(s)
    #   if s is a max node return maxValue(s)
    #   if s is an exp node return expValue(s)
    #   if s is a terminal node return evaluation(s)
    #
    # def maxValue(s)
    #   values = [value(s') for s' in successors(s)]
    #   return max(values)
    #
    # def expValue(s)
    #   values = [value(s') for s' in successors(s)]
    #   weights = [probability(s, s') for s' in successors(s)]
    #   return expectation(values, weights)

    #unlike minimax ghost number is not necessary as a parameter
    def maxValue(gameState, treeDepth):  # pacman
      # added treeDepth == 0 as termination to stop attempting to reach nonexistant index, isWin/isLose basic terminations
      if gameState.isWin() or gameState.isLose() or treeDepth == 0:
        return self.evaluationFunction(gameState)
      pacActions = gameState.getLegalActions(0)  # gets pacmans actions
      maxVal = -float("inf")  # initiates at this value to allow comparison to actually pick the max
      for moveChoice in pacActions:
        newMax = maxVal
        # generateSuccessor uses pacman's next move
        # maxVal uses the successor, depth, and 1 to reference that in the agent list ghosts are >= 1
        maxVal = max(newMax, expValue(gameState.generateSuccessor(0, moveChoice), treeDepth, 1))
        #selects new max through max function using expected value vs max value
      return maxVal #function returns maxValue that's used in expValue

    def expValue(gameState, treeDepth, agentIndex):
      # added treeDepth == 0 as termination to stop attempting to reach nonexistant index, isWin/isLose basic terminations
      if gameState.isWin() or gameState.isLose() or treeDepth == 0:
        return self.evaluationFunction(gameState)
      # expVal = float("inf")  # allows comparison to always pick the min, not needed in expValue
      ghostMoves = gameState.getLegalActions(agentIndex)
      ghostNum = gameState.getNumAgents() - 1 #don't need as a parameter but need in order to find moves for all agents not pacman
      ghostMovesNum = len(ghostMoves) #number of moves that ghosts can make
      expVal = 0 #expValue sums up the values of the nodes and later divides them for a distribution
      for move in ghostMoves:
        if (agentIndex == ghostNum):
          expVal += maxValue(gameState.generateSuccessor(agentIndex, move), treeDepth - 1)
        else:
          expVal += expValue(gameState.generateSuccessor(agentIndex, move), treeDepth, agentIndex + 1)

      return expVal/ghostMovesNum
      # expValue() calculates values and weights, the weights are expressed through ghostMovesNum and divides the values
      # from each chance node in order to return the probability distribution

    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)
    moves = gameState.getLegalActions()
    # ghostNum = gameState.getNumAgents() - 1  # since pacman is index 0 this gives ghost number, not needed here
    maxChoice = Directions.STOP  # initiate on always legal state since basically neutral
    newScore = -float("inf")  # ensures first score chooses the max between score and what minvalue returns
    for nextMove in moves:  # loop initiates to choose which actions to take
      score = newScore
      # finds expMove based off pacman's first move and self.treedepth and then gets max in order to choose what pacman does
      newScore = max(score, expValue(gameState.generateSuccessor(0,nextMove), self.treeDepth, 1))

      if newScore > score:
        maxChoice = nextMove

    return maxChoice

    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    Pretty much used what was done in the earlier evaluation function, uses spots where there is food and their
    manhattan distance in order to give incentive for pacman to collect food, distance between pacman and ghosts at
    every state is achieved through use of a while loop unlike for loops from earlier because we are not using a list
    to keep track of movements, if a capsule is available there is also incentive for pacman to move towards those spots
    numbers are for the most part arbitrary multiples of 5 again

    After submitting through autograder I found that by checking for more factors pacman lost more than winning so I
    commented that out unless I can figure out a better way for Pacman to check
  """
  "*** YOUR CODE HERE ***"
  if currentGameState.isWin():
    return float("inf")
  if currentGameState.isLose():
    return -float("inf")
  score = currentGameState.getScore()
  oldFood = currentGameState.getFood()
  currentPos = currentGameState.getPacmanPosition()
  foodSpots = oldFood.asList()
  nearbyFood = float("inf")#in order to let the for loop set a new value on first iteration
  ghostNum = currentGameState.getNumAgents() - 1
  capsuleList = currentGameState.getCapsules()

  for foodSpot in foodSpots:  # iterates through food location to find ideal food to go to next
    pacFoodDist = util.manhattanDistance(currentPos, foodSpot)
    if pacFoodDist < nearbyFood:
      nearbyFood = pacFoodDist

  # agent = 1
  # nextGhostDist = float("inf") #in order to get shortest distant to nearest ghost, starts at inf
  # while ghostNum >= agent:
  #   pacGhostDist = util.manhattanDistance(currentPos, currentGameState.getGhostPosition(agent))
  #   pacGhostDist = min(pacGhostDist, nextGhostDist)
  #   agent += 1
  #
  # score += max(pacGhostDist, 5) * 2
  # # score += pacGhostDist
  #
  # if currentGameState.getPacmanPosition() in capsuleList:
  #   score += 50

  score -= len(foodSpots) *25
  score -= 25*nearbyFood

  return score

  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

