#STUDENT NAME: Alexandre Cotorobai
#STUDENT NUMBER: 107849

#DISCUSSED TPI-1 WITH: (names and numbers):

import math

from tree_search import *

class OrderDelivery(SearchDomain):

    def __init__(self,connections, coordinates):
        self.connections = connections
        self.coordinates = coordinates
        # ANY NEEDED CODE CAN BE ADDED HERE

    def actions(self,state):
        city = state[0]
        actlist = []
        for (C1,C2,D) in self.connections:
            if (C1==city):
                actlist += [(C1,C2)]
            elif (C2==city):
               actlist += [(C2,C1)]
        return actlist 

    def result(self,state,action):
        
        (C1,C2) = action
        if C1==state[0]:
            return (C2, state[1].copy())
        

    def satisfies(self, state, goal):
        if state[0] in state[1]:
            state[1].remove(state[0])
        return state == goal
        

    def cost(self, state, action):
        # print("STATE ", state, "ACTION ", action)
        (A1, A2) = action
        for (C1, C2, D) in self.connections:
            if (C1, C2) in [(A1, A2), (A2, A1)]:
                return D

    def heuristic(self, state, goal):
        current_city = state[0]
        total_distance = 0
        destinies_not_visited = state[1].copy()

        while len(destinies_not_visited) > 0:
            min_distance = math.inf
            min_city = None
            for city in destinies_not_visited:
                distance = self.distance(current_city, city)
                if distance <= min_distance:
                    min_distance = distance
                    min_city = city
            total_distance += min_distance
            current_city = min_city
            destinies_not_visited.remove(min_city)
        
        total_distance += self.distance(current_city, goal[0])
        return int(total_distance)

    def distance (self, city1, city2):
        x1, y1 = self.coordinates[city1]
        x2, y2 = self.coordinates[city2]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) 
    



class MyNode(SearchNode):

    def __init__(self,state,parent,depth=0,cost=0,heuristic=0,arg6=None):
        super().__init__(state,parent)
        #ADD HERE ANY CODE YOU NEED
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.eval = cost + heuristic

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',maxsize=None):
        super().__init__(problem,strategy)
        #ADD HERE ANY CODE YOU NEED
        self.terminals = 1
        root = MyNode(problem.initial, None)
        self.open_nodes = [root]
        self.maxsize = maxsize
        

    def astar_add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key=lambda node: (node.eval, node.state)) 


    def search2(self):
        while self.open_nodes != []:
            
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                return self.get_path(node)
            self.non_terminals += 1
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    newnode = MyNode(newstate,
                                         node,
                                         node.depth+1,
                                         node.cost+self.problem.domain.cost(node.state,a),
                                         self.problem.domain.heuristic(newstate,self.problem.goal)
                                         )
                    lnewnodes.append(newnode)
                    # print("MAX:", len(self.open_nodes) + self.non_terminals)
                if self.maxsize != None and  self.strategy == 'A*' and len(self.open_nodes) + self.non_terminals + len(lnewnodes) > self.maxsize:
                    self.manage_memory(len(lnewnodes))
            self.add_to_open(lnewnodes)
            
        return None

    def manage_memory(self, new_nodes):
        # if len(self.open_nodes) > self.maxsize:
        # self.open_nodes.sort(key=lambda node: node.eval, reverse=True)
        open_nodes_copy = self.open_nodes.copy()
        open_nodes_copy.sort(key=lambda node: node.eval, reverse=True)
        marked_nodes = {}
        
        while len(self.open_nodes) + self.non_terminals + new_nodes > self.maxsize:
            node = open_nodes_copy.pop(0)
            # node = self.open_nodes.pop(len(self.open_nodes) - 1)
            
            parent = node.parent

            if parent is None:
                continue
            
            ## marcar node para eliminar
            if parent not in marked_nodes:
                marked_nodes[parent] = [node]
            else:
                marked_nodes[parent].append(node)
            
            ## Ver o numero de irmaos que existem
            siblings = []
            for searching_node in self.open_nodes:
                if searching_node.parent == parent:
                    siblings.append(searching_node)
            # for searching_node in marked_nodes[parent]:
            #     count += 1

            # print(count, len(marked_nodes[parent]))
            if len(siblings) == len(marked_nodes[parent]):
                # Se os siblings já estao todos marcados para deletar
                parent.eval = min([node.eval for node in marked_nodes[parent]])
                
                for node in marked_nodes[parent]:
                    if node in self.open_nodes:
                        self.open_nodes.remove(node)
                    
                    
                if parent not in self.open_nodes:
                    self.open_nodes.append(parent)
                    self.non_terminals -= 1
                marked_nodes.pop(parent)
            
        self.open_nodes.sort(key=lambda node: (node.eval, node.state))
            
            
    # if needed, auxiliary methods can be added here

def orderdelivery_search(domain,city,targetcities,strategy='breadth',maxsize=None):

    problem = SearchProblem(domain,(city, targetcities),(city,[]))
    tree = MyTree(problem,strategy,maxsize)
    tree.search2()

    path = tree.get_path(tree.solution)
    clean_path = [city for city,v in path]
    return (tree, clean_path)

# If needed, auxiliary functions can be added here


