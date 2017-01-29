# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def startingState(self):
    """
    Returns the start state for the search problem 
    """
    util.raiseNotDefined()

  def isGoal(self, state): #isGoal -> isGoal
    """
    state: Search state

    Returns True if and only if the state is a valid goal state
    """
    util.raiseNotDefined()

  def successorStates(self, state): #successorStates -> successorsOf
    """
    state: Search state
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    util.raiseNotDefined()

  def actionsCost(self, actions): #actionsCost -> actionsCost
    """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
    """
    util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successorStates(problem.startingState())
  """
  #util.raiseNotDefined()

  fringe = util.Stack() #uses the stack data structure provided in util.py
  fringe.push((problem.startingState(), [], [])) #initial state
  while fringe:
    vertex, moves, visited = fringe.pop()

    for location, direction, steps in problem.successorStates(vertex):
      if location not in visited:
        if problem.isGoal(location):
          return moves + [direction]
        fringe.push((location, moves + [direction], visited + [vertex]))

  #problem.startingState()
  #problem.isGoal(problem.startingState())
  #problem.successorStates(problem.startingState())
  return []

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  # util.raiseNotDefined()
  fringe = util.Queue() #breadthFirst uses queue
  fringe.push((problem.startingState(), [])) #initial
  visited = []
  while fringe:
    vertex, moves = fringe.pop()

    for location, direction, steps in problem.successorStates(vertex):
      if location not in visited:
        if problem.isGoal(location):
          # print moves + [direction]
          return moves + [direction]
        fringe.push((location, moves + [direction]))
        visited.append(location)
        # print visited

  return []
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  # util.raiseNotDefined()
  fringe = util.PriorityQueue()
  fringe.push((problem.startingState(), []), 0)
  visited = []

  while fringe:
    vertex, cost = fringe.pop()

    # if vertex not in visited:
    #   visited.append(vertex)

    if problem.isGoal(vertex):
      return cost

    visited.append(vertex)

    for location, direction, steps in problem.successorStates(vertex):
      if location not in visited:
        newCost = cost + [direction]
        fringe.push((location, newCost), problem.actionsCost(newCost))

  return []


def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  # util.raiseNotDefined()

  fringe = util.PriorityQueue()
  start = problem.startingState()
  closedSet = []
  fringe.push((start, []),heuristic(start, problem))

  while fringe:
    vertex, cost = fringe.pop()

    if problem.isGoal(vertex):
      return cost

    closedSet.append(vertex)

    for location, direction, moves in problem.successorStates(vertex):
      if location not in closedSet:
        newCost = cost + [direction]
        priority = problem.actionsCost(newCost) + heuristic(location, problem)
        fringe.push((location, newCost), priority)

  return []
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
