"""
File: linkedbst.py
Author: Ken Lambert
"""
from math import log2
import random
import time
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            str_ = ""
            if node is not None:
                str_ += recurse(node.right, level + 1)
                str_ += "| " * level
                str_ += str(node.data) + "\n"
                str_ += recurse(node.left, level + 1)
            return str_

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree." "")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = "L"
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = "L"
                current_node = current_node.left
            else:
                direction = "R"
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None and not current_node.right is None:
            lift_max_in_left_subtree_to_top(current_node)
        else:
            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == "L":
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def get_height(top):
            """
            Helper function
            :param top:
            :return:
            """
            if top is None:
                return -1

            subtrees = [top.left, top.right]
            return max((get_height(node) for node in subtrees), default=-1) + 1

        # if top is None:
        #     top = self._root
        return get_height(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """
        return self.height() < 2 * log2(self._size + 1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        found_elems = [item for item in range(low, high + 1) if self.find(item)]
        return found_elems

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """

        def array_to_bst(array):
            """
            Helper function to balance the tree and add the element,\
            which is located in the middle of sorted list.
            """
            if not array:
                return None

            mid_item = len(array) // 2
            root = BSTNode(array[mid_item])
            root.left = array_to_bst(array[:mid_item])
            root.right = array_to_bst(array[(mid_item + 1) :])

            return root

        tree_items = list(self.inorder())
        tree_items.sort()
        self._root = array_to_bst(tree_items)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        successor_found = None
        for node in self.inorder():
            if successor_found is None and node > item:
                successor_found = node
            elif successor_found is not None and (
                successor_found > node and node > item
            ):
                successor_found = node
        return successor_found

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        predecessor_found = None
        for node in self.inorder():
            if predecessor_found is None and node < item:
                predecessor_found = node
            elif predecessor_found is not None and (
                predecessor_found < node and node < item
            ):
                predecessor_found = node
        return predecessor_found

    @staticmethod
    def get_file_data(path):
        with open(path, "r", encoding="utf-8") as file:
            data = file.readlines()
        return data

    @staticmethod
    def get_random_words(path, num=10000):
        data = LinkedBST.get_file_data(path)
        WORDS = random.sample(data, num)
        return WORDS

    @staticmethod
    def search_list(words, file_data):
        start = time.time()
        for word in words:
            file_data.index(word)
        return time.time() - start

    @staticmethod
    def search_bst(words, file_data, should_shuffle=False, should_rebalance=False):
        if should_shuffle:
            random.shuffle(file_data)

        tree = LinkedBST()
        for word in words:
            tree.add(word)

        if should_rebalance:
            tree.rebalance()

        start = time.time()
        for word in words:
            tree.find(word)

        return time.time() - start

    def demo_bst(self, path="words.txt"):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        random_words = LinkedBST.get_random_words(path)
        file_data = LinkedBST.get_file_data(path)
        durations = (
            LinkedBST.search_list(random_words, file_data),
            LinkedBST.search_bst(random_words, file_data),
            LinkedBST.search_bst(random_words, file_data, True),
            LinkedBST.search_bst(random_words, file_data, False, True),
        )

        print(
            f"List search took: {durations[0]}sec. \n\
BST search for ordered dictionary took: {durations[1]}sec.\n\
BST search for shuffled dictionary took: {durations[2]}sec. \n\
BST search for balanced dictionary took: {durations[3]}sec."
        )


if __name__ == "__main__":
    tree_search = LinkedBST()
    tree_search.demo_bst()
