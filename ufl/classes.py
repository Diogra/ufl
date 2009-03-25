"""This file is useful for external code like tests and form compilers,
since it enables the syntax "from ufl.classes import FooBar" for getting
implementation details not exposed through the default ufl namespace."""

__authors__ = "Martin Sandve Alnes"
__date__ = "2008-08-15 -- 2009-03-25"

# Modified by Anders Logg, 2008

from ufl.expr import Expr, Operator, WrapperType, AlgebraOperator
from ufl.terminal import Terminal, FormArgument, UtilityType, Tuple
from ufl.constantvalue import ConstantValue, Zero, ScalarValue, FloatValue, IntValue, ScalarSomething, Identity
from ufl.variable import Variable, Label
from ufl.finiteelement import FiniteElementBase, FiniteElement, MixedElement, VectorElement, TensorElement
from ufl.basisfunction import BasisFunction, TestFunction, TrialFunction
from ufl.function import Function, ConstantBase, VectorConstant, TensorConstant, Constant
from ufl.geometry import GeometricQuantity, SpatialCoordinate, FacetNormal
from ufl.indexing import MultiIndex, Indexed, IndexBase, Index, FixedIndex, IndexSum
from ufl.tensors import ListTensor, ComponentTensor
from ufl.algebra import Sum, Product, Division, Power, Abs
from ufl.tensoralgebra import CompoundTensorOperator, Transposed, Outer, Inner, Dot, Cross, Trace, Determinant, Cofactor, Inverse, Deviatoric, Skew
from ufl.mathfunctions import MathFunction, Sqrt, Exp, Ln, Cos, Sin
from ufl.restriction import Restricted, PositiveRestricted, NegativeRestricted
from ufl.differentiation import Derivative, CompoundDerivative, FunctionDerivative, SpatialDerivative, VariableDerivative, Grad, Div, Curl, Rot
from ufl.conditional import Condition, EQ, NE, LE, GE, LT, GT, Conditional
from ufl.form import Form
from ufl.integral import Measure, Integral

# Make sure we import exproperators which attaches special functions to Expr
from ufl import exproperators as __exproperators

# Collect all classes in lists
__all_classes       = (c for c in locals().values() if isinstance(c, type))
all_ufl_classes     = set(c for c in __all_classes if issubclass(c, Expr))
abstract_classes    = set(s for c in all_ufl_classes for s in c.mro()[1:-1])
abstract_classes.remove(Function)
ufl_classes         = set(c for c in all_ufl_classes if c not in abstract_classes)
terminal_classes    = set(c for c in all_ufl_classes if issubclass(c, Terminal))
nonterminal_classes = set(c for c in all_ufl_classes if not issubclass(c, Terminal))

# Add _uflclass and _classid to all classes:
from ufl.common import camel2underscore as _camel2underscore
for _i, _c in enumerate(all_ufl_classes):
    _c._classid = _i
    _c._uflclass = _c
    _c._handlername = _camel2underscore(_c.__name__)

#__all__ = all_ufl_classes

