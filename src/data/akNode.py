class AkNode(object):
    def __init__(self, name, parent=None):

        self._name = name
        self._children = []
        self._parent = parent

        if parent is not None:
            parent.add_child(self)

    @staticmethod
    def type_node():
        return "NODE"

    def add_child(self, child):
        self._children.append(child)

    def children(self):
        return self._children

    def insert_child(self, position, child):

        if position < 0 or position > len(self._children):
            return False

        self._children.insert(position, child)
        child._parent = self
        return True

    def remove_child(self, position):

        if position < 0 or position > len(self._children):
            return False

        child = self._children.pop(position)
        child._parent = None

        return True

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]

    def child_count(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def grand_parent(self):
        if self.parent() is not None:
            return self.parent().parent()

        return None

    def row(self):
        if self.parent() is not None:
            return self.parent().children().index(self)

    def log(self, tab_level=-1):

        output = ""
        tab_level += 1

        for i in range(tab_level):
            output += "\t"

        output += "|------" + self._name + "\n"

        for child in self._children:
            output += child.log(tab_level)

        tab_level -= 1
        output += "\n"

        return output
