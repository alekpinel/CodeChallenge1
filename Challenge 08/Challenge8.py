# coding=utf-8
'''
  15/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 8 - Awesome Sales Inc.!
'''

# This problem is isomorphic to the famous 'Articulation Points' problem.
# So to solve it we used the implementation of an O(V+E) algorithm found in
# https://www.geeksforgeeks.org/articulation-points-or-cut-vertices-in-a-graph/

from collections import defaultdict

# This class represents an undirected graph 
# using adjacency list representation
class Graph:
   
    def __init__(self, vertices):
        self.V = vertices # No. of vertices
        self.graph = defaultdict(list) # default dictionary to store graph
        self.Time = 0
   
    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
   
    '''A recursive function that find articulation points 
    using DFS traversal
    u --> The vertex to be visited next
    visited[] --> keeps track of visited vertices
    disc[] --> Stores discovery times of visited vertices
    parent[] --> Stores parent vertices in DFS tree
    ap[] --> Store articulation points'''
    def APUtil(self, u, visited, ap, parent, low, disc):
  
        # Count of children in current node 
        children = 0
  
        # Mark the current node as visited and print it
        visited[u]= True
  
        # Initialize discovery time and low value
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
  
        # Recur for all the vertices adjacent to this vertex
        for v in self.graph[u]:
            # If v is not visited yet, then make it a child of u
            # in DFS tree and recur for it
            if visited[v] == False :
                parent[v] = u
                children += 1
                self.APUtil(v, visited, ap, parent, low, disc)
  
                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                low[u] = min(low[u], low[v])
  
                # u is an articulation point in following cases
                # (1) u is root of DFS tree and has two or more children.
                if parent[u] == -1 and children > 1:
                    ap[u] = True
  
                #(2) If u is not root and low value of one of its child is more
                # than discovery value of u.
                if parent[u] != -1 and low[v] >= disc[u]:
                    ap[u] = True    
                      
                # Update low value of u for parent function calls    
            elif v != parent[u]: 
                low[u] = min(low[u], disc[v])
  
  
    # The function to do DFS traversal. It uses recursive APUtil()
    def AP(self):
        # Mark all the vertices as not visited 
        # and Initialize parent and visited, 
        # and ap(articulation point) arrays
        visited = [False] * (self.V)
        disc = [float("Inf")] * (self.V)
        low = [float("Inf")] * (self.V)
        parent = [-1] * (self.V)
        ap = [False] * (self.V) # To store articulation points
  
        # Call the recursive helper function
        # to find articulation points
        # in DFS tree rooted with vertex 'i'
        for i in range(self.V):
            if visited[i] == False:
                self.APUtil(i, visited, ap, parent, low, disc)
  
        return ap

def getCriticalCitiesThatCannotBeRemoved(case):
    cities = []
    numberByCity = {}
    for ticket in case:
        if (ticket[0] not in numberByCity):
            numberByCity[ticket[0]] = len(cities)
            cities.append(ticket[0])
            
        if (ticket[1] not in numberByCity):
            numberByCity[ticket[1]] = len(cities)
            cities.append(ticket[1])
    
    # print (cities)
    # print (numberByCity)
    nCities = len(cities)
    
    graph = Graph(nCities)
    for ticket in case:
        graph.addEdge(numberByCity[ticket[0]], numberByCity[ticket[1]])
    
    criticalIndices = graph.AP()
    
    criticalCities = []
    for i in range(nCities):
        if (criticalIndices[i]):
            criticalCities.append(cities[i])
            
    criticalCities.sort()
    
    result = ''
    if (len(criticalCities) > 0):
        result = criticalCities[0]
        for city in criticalCities[1:]:
            result += ',' + city
    else:
        result = '-'
    
    return result

def processCase(case):
    # print (case)
    return getCriticalCitiesThatCannotBeRemoved(case)
    
def readCase(file):
    nEdges = int(file.readline().replace('\n', ''))
    case = []
    for i in range(nEdges):
        ticket = file.readline().replace('\n', '').split(',')
        case.append(ticket)
    return case

#Get input
def readInput(inputfile, caseProcessor):
    f = open(inputfile + ".txt", "r", encoding="utf-8")
    nlines = int(f.readline())
    lines = []
    for i in range(nlines):
        lines.append(caseProcessor(f))
    f.close()
    return lines

#Write the output
class OutputWriter:
    def __init__(self, outputfile):
        self.outputfile = None if outputfile == None else open(outputfile + ".txt", "w", encoding="utf-8");
        self.i = 0
        
    def __del__(self):
        if (self.outputfile != None):
            self.outputfile.close()

    def __call__(self, output):
        string = "Case #" + str(self.i + 1) + ": " + str(output) + "\n"
        self.i = self.i + 1
        print(string.replace("\n", ""))
        if (self.outputfile != None):
            self.outputfile.write(string)

def main():
    testType = 'submit'
    writeFile = True

    inputfile = testType + "Input"
    outputfile = testType + "Output"

    if (not writeFile):
        outputfile = None

    inputs = readInput(inputfile, readCase)


    outputWriter = OutputWriter(outputfile)
    for input in inputs:
        output = getCriticalCitiesThatCannotBeRemoved(input)
        outputWriter(output)

if __name__ == "__main__":
    main()
