class AkNode(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._children = []
        self._parent = parent

        if (parent is not None):
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    def getName(self):
        return self._name

    def getChild(self, row):
        return self._children[row]

    def getChildCount(self):
        return len(self._children)

    def getParent(self):
        return self._parent

    def getRow(self):
        if (self._parent is not None):
            return self._parent._children.index(self)


    def log(self, tabLevel=-1):
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "\t"

        output += "|---" + self._name + "\n"

        for child in self._children:
            output += child.log(tabLevel)

        tabLevel -= 1
        output += "\n"

        return output

    def __repr__(self):
        return self.log()


if __name__ == '__main__':
    tato = AkNode('Andriy')
    child1 = AkNode("Kolya", tato)
    child2 = AkNode("Dima", tato)
    subChild1 = AkNode("Marina", child1)

    print(tato)