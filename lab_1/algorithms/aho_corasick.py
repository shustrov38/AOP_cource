from typing import Tuple, List


comparisons_count = 0


class Node:

    def __init__(self, edges: List[int] = [], leaf: int = -1, 
                 link: int = 0, parent: int = -1, char: str = ''):
        self.edges = edges.copy()
        self.leaf = leaf
        self.link = link
        self.parent = parent
        self.char = char

    def __repr__(self) -> str:
        return self.char


class AhoCorasick:

    def __init__(self):
        self.nodes = [Node()]
        self.patterns = []

    def add_pattern(self, pattern: str) -> None:
        v = 0

        if len(pattern) == 0:
            return
        
        for ch in pattern:
            next_step = -1

            for x in self.nodes[v].edges:
                if ch == self.nodes[x].char:
                    next_step = x
                    break

            if next_step == -1:
                new_node = Node(parent=v, char=ch)
                self.nodes.append(new_node)
                next_step = len(self.nodes) - 1
                self.nodes[v].edges.append(next_step)
                
            v = next_step

        self.patterns.append(pattern)
        self.nodes[v].leaf = len(self.patterns) - 1

    def set_links(self) -> None:
        queue = [0]
        while len(queue) != 0:
            node_id = queue.pop(0)
            for x in self.nodes[node_id].edges:
                if self.nodes[x].parent != 0:
                    node = self.nodes[x]
                    parent_link = self.nodes[node.parent].link
                    for y in self.nodes[parent_link].edges:
                        if node.char == self.nodes[y].char:
                            self.nodes[x].link = y
                            break
                    if self.nodes[x].link == 0:
                        if self.nodes[x].char == self.nodes[parent_link].char:
                            self.nodes[x].link = parent_link
                        else:
                            for y in self.nodes[0].edges:
                                if self.nodes[x].char == self.nodes[y].char:
                                    self.nodes[x].link = y
                queue.append(x)

    def search(self, text: str) -> List[Tuple[str, int]]:
        global comparisons_count
        text_size = len(text)

        if text_size == 0:
            return -1
        
        ans = []
        v, i = 0, 0
        while True:
            if self.nodes[v].leaf != -1:
                pattern = self.patterns[self.nodes[v].leaf]
                ans.append((pattern, i - len(pattern)))

            if self.nodes[self.nodes[v].link].leaf != -1:
                pattern = self.patterns[self.nodes[self.nodes[v].link].leaf]
                ans.append((pattern, i - len(pattern)))

            if i == text_size:
                break

            next_step = -1
            for x in self.nodes[v].edges:
                comparisons_count += 1
                if text[i] == self.nodes[x].char:
                    next_step = x
                    break

            if next_step == -1:
                if v == 0:
                    i += 1
                v = self.nodes[v].link
            else:
                v = next_step
                i += 1
        return ans


def search(text: str, pattern: str) -> Tuple[int, int]:
    global comparisons_count
    comparisons_count = 0
    text_size = len(text)
    pattern_size = len(pattern)

    if pattern_size == 0:
        return 0, 0
    
    if text_size == 0 or pattern_size > text_size:
        return -1, 0
    
    trie = AhoCorasick()
    trie.add_pattern(pattern=pattern)
    trie.set_links()
    _, i = trie.search(text)[0]

    return i, comparisons_count
