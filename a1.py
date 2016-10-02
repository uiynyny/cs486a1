class Vertex:
   def __init__(self, node):
       self.id = node
       self.parent=None
       self.adj = {}

   def add_neighbor(self, neighbor, weight=0):
       self.adj[neighbor] = weight

   def get_connections(self):
       return self.adj.keys()

   def get_neighbor(self):
       return self.adj

   def get_weight(self, neighbor):
       return self.adj[neighbor]
class Graph:
   def __init__(self):
       self.vert_dict = {}
       self.num_vert = 0

   def __iter__(self):
       return iter(self.vert_dict.values())

   def add_vertex(self, node):
       self.num_vert += 1
       new_vertex = Vertex(node)
       self.vert_dict[node] = new_vertex
       return new_vertex

   def get_vertex(self, n):
       if n in self.vert_dict:
           return self.vert_dict[n]
       else:
           return None

   def add_edge(self, origin, dest, cost=0):
       if origin not in self.vert_dict:
           self.add_vertex(origin)
       if dest not in self.vert_dict:
           self.add_vertex(dest)
       self.vert_dict[origin].add_neighbor(self.vert_dict[dest], cost)

   def get_vertices(self):
       return self.vert_dict.keys()
def BFS_method(v, pattern):
   queue = []
   result = []
   queue.append(v)
   considered = 1
   v.prob = 1.0
   v.parent = None
   while queue:
       current = queue.pop(0)
       cur_pattern = pattern.index(current.id.split('/')[1])
       if cur_pattern+1 == len(pattern):
           result.append(current)
       if cur_pattern+1 < len(pattern):
           for key in current.adj:
               if key.id.split('/')[1] == pattern[cur_pattern+1]:
                   tempprob = current.prob * current.adj[key]
                   if key.parent is None:
                       key.parent = current
                       key.prob=tempprob
                       queue.append(key)
                   elif tempprob > key.prob:
                       key.parent = current
                       key.prob=tempprob
                   considered += 1
   for i in result:
       temp=i
       while temp is not None:
           print(temp.id, end=' ')
           temp=temp.parent
       print(i.prob)
   print(considered)

def generate(start, pattern, graph):
   g = Graph()
   for line in graph:
       lists = line.split("//")
       g.add_edge(lists[0], lists[1], float(lists[2]))
   curWord = start + "/" + pattern[0]
   v = g.get_vertex(curWord)

   # BFS method
   BFS_method(v, pattern)
if __name__ == '__main__':
   file = open("input.txt")
   startingWord = 'hans'
   sentenceSpec = ['NNP', 'VBD', 'DT', 'NN']
   generate(startingWord, sentenceSpec, file)

