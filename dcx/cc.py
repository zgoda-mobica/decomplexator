"""
@author: Simone Papandrea

Cleaned a bit by Jarek Zgoda
"""

import redbaron

redbaron.ipython_behavior = False


class CognitiveComplexity(object):

    def evaluate(self, filename):
        """
        Calculate cognitive complexity for all functions and methods defined in file.
        """
        fns = dict()
        with open(filename) as file:
            red = redbaron.RedBaron(file.read())

            for fn in red.find_all("def"):
                names = []
                p = fn
                while p:
                    names = [p.name] + names
                    p = p.parent_find(['def', 'class'])
                name = '.'.join(names)
                cc = self.__sequences(fn) + self.__conditions(fn) + self.__structures(fn)
                fns[name] = cc
        return fns

    def __sequences(self, func):
        cc = 0
        last = None
        for node in func.find_all("BooleanOperatorNode"):
            if last is None or node.value != last.value or node.parent_find(last) is None:
                cc += 1

            if 'not' in [node.value for node in node.find_all("UnitaryOperatorNode")]:
                cc += 1

            last = node
        return cc

    def __conditions(self, func):
        return len(func.find_all("ElifNode")) + len(func.find_all("ElseNode"))

    def __structures(self, func):

        increments = {
            "IfNode",
            "TernaryOperatorNode",
            "ComprehensionIfNode",
            "ForNode",
            "ComprehensionLoopNode",
            "WhileNode",
            "ExceptNode"
        }
        levels = increments.union({
            "ElseNode",
            "ElifNode",
            "DefNode",
            "LambdaNode"
        })
        nodes = list()

        for node in increments:
            nodes.extend(func.find_all(node))

        cc = 0
        for node in nodes:
            node = node.parent
            while node != func.parent:
                name = node.__class__.__name__
                if name in levels and (name != 'DefNode' or not self.__is_decorator(node)):
                    cc += 1
                node = node.parent
        return cc

    def __is_decorator(self, func):
        values = [
            node.__class__.__name__
            for node in func.value
            if node.__class__.__name__ not in ['CommentNode', 'EndlNode']
        ]
        return len(values) == 2 and values[0] == 'DefNode' and values[1] == 'ReturnNode'
