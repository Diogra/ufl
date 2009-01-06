"""This module defines partial differentiation rules for
all relevant operands for use with reverse mode AD."""

__authors__ = "Martin Sandve Alnes"
__date__ = "2009-01-06 -- 2009-01-06"

from ufl.output import ufl_assert, ufl_error
from ufl.classes import Zero, IntValue, FloatValue
from ufl.operators import sin, cos, exp, ln, sqrt
from ufl.tensors import unit_vectors
from ufl.conditional import sign
from ufl.algorithms.transformations import Transformer

class PartialDerivativeComputer(Transformer):
    """NB! The main reason for keeping this out of the Expr hierarchy is
    to avoid user mistakes in the form of mixups with total derivatives,
    and to allow both reverse and forward mode AD."""
    #def __init__(self, spatial_dim):
    def __init__(self):
        Transformer.__init__(self)
        #self._spatial_dim = spatial_dim
    
    # TODO: Make sure we have implemented partial derivatives of all operators. At least non-compound ones should be covered, but compound ones may be a good idea in future versions.
    
    # --- Basic algebra operators
    
    def sum(self, f):
        "d/dx_i sum_j x_j = 1"
        _1 = IntValue(1) # TODO: Handle non-scalars
        return tuple(_1 for o in f.operands())
    
    def product(self, f):
        a, b = f.operands() # TODO: Assuming binary operator for now
        da = b # TODO: Is this right even for non-scalar b? And implicit sums?
        db = a
        return (da, db)
    
    def division(self, f):
        """f = x/y
        d/dx x/y = 1/y
        d/dy x/y = -x/y**2 = -f/y"""
        x, y = f.operands()
        d = 1/y
        return (d, -f*d)
    
    def power(self, f):
        """f = x**y
        d/dx x**y = y*x**(y-1) = y*f/x
        d/dy x**y = ln(x)*x**y = ln(x)*f"""
        x, y = f.operands()
        dx = y*f/x
        dy = ln(x)*f
        return (dx, dy)
    
    def abs(self, f):
        """f = |x|
        d/dx |x| = { +1, if x > 0
                   { -1, if x < 0
                   {  0, if x == 0 (not strictly correct, but better than leaving it undefined?)
        """
        x, = f.operands()
        dx = sign(x) 
        return (dx,)
    
    # --- Mathfunctions
    
    def sqrt(self, f):
        "d/dx sqrt(x) = 1 / (2*sqrt(x))"
        return (0.5/f,)
    
    def exp(self, f):
        "d/dx exp(x) = exp(x)"
        return (f,)
    
    def ln(self, f):
        "d/dx ln x = 1 / x"
        x, = f.operands()
        return (1/x,)
    
    def cos(self, f):
        "d/dx cos x = -sin(x)"
        x, = f.operands()
        return (-sin(x),)
    
    def sin(self, o, a):
        "d/dx sin x = cos(x)"
        x, = f.operands()
        return (cos(x),)
    
    # --- Shape and indexing manipulators
    
    def indexed(self, f):
        "d/dx x_i = (1)_i = 1" # TODO: Is this right? Fix for non-scalars too.
        s = f.shape()
        ufl_assert(s == (), "TODO: Assuming a scalar expression.")
        _1 = IntValue(1) # TODO: Non-scalars
        return (_1, None)
    
    def list_tensor(self, f):
        "d/dx_i [x_0, ..., x_n-1] = e_i (unit vector)" # TODO: Is this right? Fix for higher order tensors too.
        ops = f.operands()
        n = len(ops)
        s = ops[0].shape()
        ufl_assert(s == (), "TODO: Assuming a vector, i.e. scalar operands.")
        return unit_vectors(n) # TODO: Non-scalars
    
    def component_tensor(self, f):
        x, i = f.operands()
        s = f.shape()
        ufl_assert(len(s) == 1, "TODO: Assuming a vector, i.e. scalar operands.")
        d = ListTensor([1]*n) # TODO: Non-scalars
        return (d, None)
    
    # --- Restrictions
    
    def positive_restricted(self, f):
        _1 = IntValue(1) 
        return (_1,) # or _1('+')? TODO: is this right?
    
    def negative_restricted(self, f):
        _1 = IntValue(1)
        return (_1,) # or _1('-')? TODO: is this right?
    
    # --- Conditionals
    
    def condition(self, f):
        return (None, None)
    
    def conditional(self, f): # TODO: Is this right? What about non-scalars?
        c, a, b = f.operands()
        s = f.shape()
        ufl_assert(s == (), "TODO: Assuming scalar valued expressions.")
        _0 = Zero()
        _1 = IntValue(1)
        da = conditional(c, _1, _0)
        db = conditional(c, _0, _1)
        return (None, da, db)
    
    # --- Derivatives
    
    def spatial_derivative(self, f):
        ufl_error("Partial derivative of spatial_derivative not implemented, when is this called? apply_ad should make sure it isn't called.")
        x, i = f.operands()
        return (None, None)
    
    def variable_derivative(self, f):
        ufl_error("Partial derivative of variable_derivative not implemented, when is this called? apply_ad should make sure it isn't called.")
        x, v = f.operands()
        return (None, None)
    
    def function_derivative(self, f):
        ufl_error("Partial derivative of function_derivative not implemented, when is this called? apply_ad should make sure it isn't called.")
        a, w, v = f.operands()
        return (None, None, None)

