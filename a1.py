from operator import attrgetter


class Vertex:
    def __init__(self, node):
        self.id = node
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


class Data:
    def __init__(self, seq, prob=1):
        self.seq = seq
        self.prob = prob

    def size(self):
        return len(self.seq)

    def get_last(self):
        return self.seq[-1]

    def toString(self):
        sentence = []
        for word in self.seq:
            sentence.append(word.id.split('/')[0])
        return ' '.join(sentence)


def BFS_method(v, pattern):
    queue = []
    result = []
    queue.append(Data([v]))
    considered = 1
    while queue:
        current = queue.pop(0)
        if current.size() == len(pattern):
            result.append(current)
        else:
            for key in current.get_last().adj:
                if key.id.split('/')[1] == pattern[current.size()]:
                    temp_prob = current.prob * current.get_last().adj[key]
                    queue.append(Data(current.seq + [key], temp_prob))
                    considered += 1
    maxItem = max(result, key=attrgetter('prob'))
    print("\"" + maxItem.toString() + "\" with probability " + str(maxItem.prob))
    print('Total nodes considered: ' + str(considered))


def DFS_method(v, pattern):
    queue = []
    result = []
    queue.append(Data([v]))
    considered = 1
    while queue:
        current = queue.pop()
        if current.size() == len(pattern):
            result.append(current)
        else:
            for key in current.get_last().adj:
                if key.id.split('/')[1] == pattern[current.size()]:
                    temp_prob = current.prob * current.get_last().adj[key]
                    queue.append(Data(current.seq + [key], temp_prob))
                    considered += 1
    maxItem = max(result, key=attrgetter('prob'))
    print("\"" + maxItem.toString() + "\" with probability " + str(maxItem.prob))
    print('Total nodes considered: ' + str(considered))


def Heuristic_search(v, pattern, h):
    queue = []
    result = []
    queue.append(Data([v]))
    considered = 0
    while queue:
        ptr = (0, None)
        queue = [x for x in queue if
                 x.size() == len(pattern) or (x.size() < len(pattern) and (x.get_last().id, pattern[x.size()]) in h)]
        for item in queue:
            if item.size() < len(pattern):
                if (item.get_last().id, pattern[item.size()]) in h:
                    if h[(item.get_last().id, pattern[item.size()])] * item.prob > ptr[0]:
                        ptr = (h[(item.get_last().id, pattern[item.size()])] * item.prob, item)
            elif item.size() == len(pattern):
                if item.prob > ptr[0]:
                    ptr = (item.prob, item)
        current = ptr[1]
        queue.remove(current)
        considered += 1
        if current.size() == len(pattern):
            result.append(current)
            break
        else:
            for key in current.get_last().adj:
                if key.id.split('/')[1] == pattern[current.size()]:
                    queue.append(Data(current.seq + [key], current.prob * current.get_last().adj[key]))
    print("\"" + result[0].toString() + "\" with probability " + str(result[0].prob))
    print('Total nodes considered: ' + str(considered))


def generate(start, pattern, search, graph):
    g = Graph()
    heuristic = {}
    for line in graph:
        lists = line.split("//")
        g.add_edge(lists[0], lists[1], float(lists[2]))
        dict_key = (lists[0], lists[1].split('/')[1])
        if dict_key in heuristic:
            if heuristic[dict_key] < float(lists[2]):
                heuristic[dict_key] = float(lists[2])
        else:
            heuristic[dict_key] = float(lists[2])
    curWord = start + "/" + pattern[0]
    v = g.get_vertex(curWord)
    if search is "BREADTH_FIRST":
        BFS_method(v, pattern)
    elif search is "D":
        DFS_method(v, pattern)
    elif search is "H":
        Heuristic_search(v, pattern, heuristic)


if __name__ == '__main__':
    file = open("input.txt")
    startingWord = "a"
    sentenceSpec = ["DT", "NN", "VBD", "NNP", "IN", "DT", "NN"]
    generate(startingWord, sentenceSpec, "B", file)
