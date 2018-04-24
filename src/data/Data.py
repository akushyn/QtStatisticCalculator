from enum import Enum


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
    series = {'D': [1,2,3,4,5,6,7], 'W': [], 'M': [], 'Q': [], 'Y': []}
    print(series['D'])

    aaa = {}
    aaa['z'] = [1,2,3]

    print(aaa)
    lst = aaa['z']
    print(lst[2])