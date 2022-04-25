
""" 
this module is intended for making a trie structure, 
that helps to implemet real time data search
"""

class TrieNode( object ):

    """ 
        trie class ment to hold keys
    """

    def __init__(self, char:str) -> None:

        self.char = char    #character for which node is intialized
        self.isEnd = False  #checks if its the end of tree
        self.follow = None  #database refrence from which future query could be pulled out

        self.counter = 0    #counts how may times word has occured
        self.children = {}  #stores all child nodes keys:characters nodes values


class Trie(object):

    def __init__(self) -> None:
        self. root = TrieNode("")   #node intialisations

    def insert(self, word:str, follow) -> None:

        """
        Function to insert data into trie
        Parameters
            word(str):word you want to insert
            follow(any):anything that you want to refrence to that word
        
        Return
            None
        """

        node = self.root    #parent node

        for char in word:

            #checking for characters in node

            if char in node.children:

                node = node.children[char] # if present adds child keys

            else:

                newNode = TrieNode(char)        #if not preset adds new node
                node.children[char] = newNode   #appends to parent node
                node = newNode                  #set the current node to the new one

        
        node.isEnd = True      #signaling for word end
        node.follow = follow   #allocating database follow along 
        node.counter += 1      #incrementing counter




    def dfs(self, node, prefix) -> list:

        """
            function for searching trie structure

            Parameters:
                node(TrieClass):leaf for which search has to take place
                prefix(str):parents that already have been traversed

            Returns:
                list [(word, count, follow)]/[]
        """

        #implementing depth first search for finding words out of structure

        if node.isEnd:

            #appends result if end of word is found

            self.output.append((prefix + node.char, node.counter, node.follow))

        for child in node.children.values():

            #searches for word in recurssion fashion

            self.dfs(child, prefix + node.char)


    def addQuery(self, x:str):
        """ 
            Helper function for adding query by lowercasing them
            and breaking them on whitespaces
        """

        pass


    def query(self, x:str):

        """
        Function to query a word from class
        Parameters:
            x(str):word you want to search

        Returns:
            list [(word, count, follow)]/[]
            
        """

        self.output = []
        node = self.root  

        for char in x:
            if char in node.children:
                node = node.children[char]

            else:
                return []

        self.dfs(node, x[:-1]) #traversing word

        return sorted(self.output, key=lambda x:x[1], reverse = True) #reverse sorting in word count fashion
    

""" 
t = Trie()
t.insert("t.s.h", 1)
t.insert("testostorones", 0)
t.insert("word", 2)
t.insert("war", 3)
t.insert("what", 4)
t.insert("where", 5)

print(t.query("t"))
"""