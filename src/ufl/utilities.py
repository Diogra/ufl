#!/usr/bin/env python

"""
Utility algorithms for inspection, conversion or transformation
of UFL objects in various ways.

(Currently, some utility functions are located in visitor.py,
some in traversal.py, and some in transformers.py,
depending on the method of implementation.
This file should contain userfriendly front-ends
to all the utility algorithms that we want to expose.)
"""

__version__ = "0.1"
__authors__ = "Martin Sandve Alnes"
__copyright__ = __authors__ + " (2008)"
__licence__ = "GPL" # TODO: which licence?
__date__ = "17th of December 2008"

from base import *


### Utilities to extract information from an expression:

# TODO: test performance of visitor implementations vs functional implementations

def basisfunctions(u):
    from visitor import BasisFunctionFinder
    vis = BasisFunctionFinder()
    vis.visit(u)
    # FIXME: sort by index
    return vis.basisfunctions

def coefficients(u):
    from visitor import CoefficientFinder
    vis = CoefficientFinder()
    vis.visit(u)
    # FIXME: sort by index
    return vis.coefficients

def duplications(u):
    from visitor import SubtreeFinder
    vis = SubtreeFinder()
    vis.visit(f)
    return vis.duplicated


### Utilities to convert expression to a different form:

def flatten(u):
    vis = TreeFlattener()
    return vis.visit(f)



