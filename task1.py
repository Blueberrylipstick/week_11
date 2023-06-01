"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log2
import random
import timeit
import sys

sys.setrecursionlimit(25000)


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
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                lyst.append(node.data)
                recurse(node.left)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                recurse(node.right)
                lyst.append(node.data)

        recurse(self._root)
        return iter(lyst)

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        lyst = list()
        sub_list = [self._root]
        while any(elem is not None for elem in sub_list):
            lyst.append(sub_list)
            temp = []
            for elem in sub_list:
                if elem is not None:
                    temp.append(elem.left)
                    temp.append(elem.right)
                else:
                    temp.append(None)
            sub_list = temp
        return lyst

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

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
        while True:

            if self.isEmpty():
                self._root = BSTNode(item)
                self._size += 1
                break

            else:
                parent = None
                current = self._root
                while current is not None:
                    parent = current
                    if item < current.data:
                        current = current.left
                    else:
                        current = current.right
                if item < parent.data:
                    parent.left = BSTNode(item)
                    self._size += 1
                    break
                else:
                    parent.right = BSTNode(item)
                    self._size += 1
                    break
                

        # Helper function to search for item's position
        # def recurse(node):
        #     # New item is less, go left until spot is found
        #     if item < node.data:
        #         if node.left == None:
        #             node.left = BSTNode(item)
        #         else:
        #             recurse(node.left)
        #     # New item is greater or equal,
        #     # go right until spot is found
        #     elif node.right == None:
        #         node.right = BSTNode(item)
        #     else:
        #         recurse(node.right)
        #         # End of recurse

        # # Tree is empty, so new item goes at the root
        # if self.isEmpty():
        #     self._root = BSTNode(item)
        # # Otherwise, search for the item's spot
        # else:
        #     recurse(self._root)
        # self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0
            else:
                return 1 + max(height1(top.left), height1(top.right))

        return max(height1(self._root) - 1, 0)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        # 2 * log2(n + 1) - 1

        if self.height() < 2 * log2(self._size + 1) - 1:
            return True
        return False


    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        if low > high:
            raise ValueError('wrong range, first argument should be smaller that second')
        lst = []
        inorder_lst = list(self.inorder())
        for elem in inorder_lst:
            if low <= elem <= high:
                lst.append(elem)
        return lst

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def build_balanced_tree(lst, start, end):
            if start > end:
                return None

            mid = ((start + end) // 2) + ((start + end) % 2)
            root = BSTNode(lst[mid])

            root.left = build_balanced_tree(lst, start, mid - 1)
            root.right = build_balanced_tree(lst, mid + 1, end)

            return root

        lst = list(self.inorder())
        self.clear()

        self._root = build_balanced_tree(lst, 0, len(lst) - 1)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        # if not self.find(item):
        #     return None

        # sorted_lst = list(self.inorder())
        lst = []
        for elem in self:#sorted_lst:
            if elem > item:
                lst.append(elem)
        return min(lst) if lst else None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        # if not self.find(item):
        #     return None

        lst = []
        for elem in self:
            if elem < item:
                lst.append(elem)
        return max(lst) if lst else None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        def read_file(path):
            words = []
            with open(path, encoding='utf-8') as file:
                for line in file.readlines():
                    words.append(line.strip())
            return words[:20000]

        dictionary = read_file(path)
        dictionary_random = random.sample(dictionary, len(dictionary))
        words = random.sample(dictionary, 10000)
        sorted_dict = sorted(dictionary)


        sorted_tree = LinkedBST()
        for elem in sorted_dict:
            sorted_tree.add(elem)

        unsorted_tree = LinkedBST()
        for elem in dictionary_random:
            unsorted_tree.add(elem)

        balanced_tree = LinkedBST()
        for elem in dictionary_random:
            balanced_tree.add(elem)
        balanced_tree.rebalance()

        start = timeit.default_timer()
        for word in words:
            if word in sorted_dict:
                pass
        end = timeit.default_timer()
        time_sorted_list = end - start

        start = timeit.default_timer()
        for word in words:
            if sorted_tree.find(word):
                pass
        end = timeit.default_timer()
        time_sorted_tree = end - start

        start = timeit.default_timer()
        for word in words:
            if unsorted_tree.find(word):
                pass
        end = timeit.default_timer()
        time_unsorted_tree = end - start

        start = timeit.default_timer()
        for word in words:
            if balanced_tree.find(word):
                pass
        end = timeit.default_timer()
        time_balanced_tree = end - start

        print(1)
        print(f'Time needed to find random 10000 words in a sorted dictionary: {round(time_sorted_list, 5)}')
        print(f'Time needed to find random 10000 words in a sorted binary tree: {round(time_sorted_tree, 5)}')
        print(f'Time needed to find random 10000 words in an unsorted binary tree: {round(time_unsorted_tree, 5)}')
        print(f'Time needed to find random 10000 words in a balanced binary tree: {round(time_balanced_tree, 5)}')

tree = LinkedBST()
tree.add(5)
tree.add(3)
tree.add(8)
tree.add(2)
tree.add(4)
tree.add(7)

print(tree)
print(tree.height())
print(tree.is_balanced())
print(tree.range_find(3, 7))
print(tree.successor(3))
print(tree.predecessor(3))
tree.rebalance()
print(tree)

tree.demo_bst('words.txt')