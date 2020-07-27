# -*- coding: utf-8 -*-
"""General Tree module.

"""

from . import queue
from .queue import Queue


class Tree:
    """Simple class for general tree.

    Attributes:
        key (Any): Node key.
        children (List[Tree]): Node children.

    """
    def __init__(self, key=None, children=None):
        """Init general tree, ensure children are properly set.

        Args:
            key (Any).
            children (List[Tree]).

        """

        self.key = key

        if children is None:
            self.children = []
        else:
            self.children = children

    @property
    def nbchildren(self):
        """Number of children of node."""

        return len(self.children)

