class Vertex:
    def __init__(self, node):
        self.id = node
        self.parent = None
        self.pattern = -1
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
    v.pattern = 0
    while queue:
        current = queue.pop(0)
        if current.pattern+1 == len(pattern):
            result.append(current)
            considered += 1
        else:
            for key in current.adj:
                if key.id.split('/')[1] == pattern[current.pattern+1]:
                    temp_prob = current.prob * current.adj[key]
                    if key.parent is None:
                        key.parent = current
                        key.prob = temp_prob
                        key.pattern = current.pattern+1
                        queue.append(key)
                    elif temp_prob > key.prob:
                        key.parent = current
                        key.prob = temp_prob
                        key.pattern = current.pattern+1
                    considered += 1
    # for i in queue:
    #     temp = i
    #     while temp is not None:
    #         print(temp.id, end=' ')
    #         temp = temp.parent
    #     print(i.prob)
    result.sort(key=lambda x: x.prob, reverse=True)
    sentence = []
    parent = result[0]
    prob = parent.prob
    while parent is not None:
        sentence.append(parent.id.split('/')[0])
        parent = parent.parent
    sentence.reverse()
    print("\""+' '.join(sentence)+"\" with probability "+str(prob))
    print("Total nodes considered: "+str(considered))

def DFS_method(v,pattern):
    queue = []
    result = []
    queue.append(v)
    considered = 1
    v.prob = 1.0
    v.parent = None
    v.pattern = 0
    while queue:
        current = queue.pop()
        if current.pattern + 1 == len(pattern):
            result.append(current)
            considered += 1
        else:
            for key in current.adj:
                if key.id.split('/')[1] == pattern[current.pattern + 1]:
                    temp_prob = current.prob * current.adj[key]
                    if key.parent is None:
                        key.parent = current
                        key.prob = temp_prob
                        key.pattern = current.pattern + 1
                        queue.append(key)
                    elif temp_prob > key.prob:
                        key.parent = current
                        key.prob = temp_prob
                        key.pattern = current.pattern + 1
                    considered += 1
    # for i in queue:
    #     temp = i
    #     while temp is not None:
    #         print(temp.id, end=' ')
    #         temp = temp.parent
    #     print(i.prob)
    result.sort(key=lambda x: x.prob, reverse=True)
    sentence = []
    parent = result[0]
    prob = parent.prob
    while parent is not None:
        sentence.append(parent.id.split('/')[0])
        parent = parent.parent
    sentence.reverse()
    print("\"" + ' '.join(sentence) + "\" with probability " + str(prob))
    print("Total nodes considered: " + str(considered))

def generate(start, pattern, graph):
    g = Graph()
    for line in graph:
        lists = line.split("//")
        g.add_edge(lists[0], lists[1], float(lists[2]))
    curWord = start + "/" + pattern[0]
    v = g.get_vertex(curWord)
    # BFS_method(v, pattern)
    DFS_method(v,pattern)

if __name__ == '__main__':
    file = open("input.txt")
    startingWord = "hans"
    sentenceSpec = ['NNP', 'VBD', 'DT', 'NN']
    generate(startingWord, sentenceSpec, file)
