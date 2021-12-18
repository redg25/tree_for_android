class TreeMeta(type):
    """A Tree metaclass that will be used for Tree class creation.
   """
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'update_tree') and
                callable(subclass.update_tree) and
                hasattr(subclass, 'remove_tree') and
                callable(subclass.remove_tree))

class Tree(metaclass=TreeMeta):

    """Tree interface built from PersonMeta metaclass."""

    def __init__(self):
        self.position = None
        self.tag = None
        self.type = None
        self.comments = ''


    pass

class YoungTree(Tree):
    """ Class inheriting from Tree for trees to be sold young"""

    def update_tree(self):
        pass

    def remove_tree(self):
        pass



