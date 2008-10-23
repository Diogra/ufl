"""FormData class easy for collecting of various data about a form."""

from __future__ import absolute_import

__authors__ = "Martin Sandve Alnes"
__date__ = "2008-09-13 -- 2008-10-23"

# Modified by Anders Logg, 2008

from itertools import chain

from ..output import ufl_assert
from ..common import lstr, tstr, domain_to_dim
from ..form import Form

from .analysis import extract_basisfunctions, extract_coefficients, extract_classes

class FormData(object):
    "Class collecting various information extracted from form."
    
    def __init__(self, form):
        "Create form data for given form"
        ufl_assert(isinstance(form, Form), "Expecting Form.")
        
        self.form = form

        # Get arguments and their elements
        self.basisfunctions  = extract_basisfunctions(form)
        self.coefficients    = extract_coefficients(form)
        self.elements        = [f._element for f in chain(self.basisfunctions, self.coefficients)]
        self.unique_elements = set(self.elements)
        self.domain          = self.elements[0].domain()
        
        # Some useful dimensions
        self.rank = len(self.basisfunctions)
        self.num_coefficients = len(self.coefficients)
        self.geometric_dimension = domain_to_dim(self.domain)
        self.topological_dimension = self.geometric_dimension
        
        # Build renumbering of arguments, since Function and BasisFunction
        # count doesn't necessarily match their exact order in the argument list
        def argument_renumbering(arguments):
            return dict((f,k) for (k,f) in enumerate(arguments))
        self.basisfunction_renumbering = argument_renumbering(self.basisfunctions)
        self.coefficient_renumbering = argument_renumbering(self.coefficients)
        
        # The set of all UFL classes used in each integral,
        # can be used to easily check for unsupported operations
        self.classes = {}
        for i in form.cell_integrals():
            self.classes[i] = extract_classes(i._integrand)
        for i in form.exterior_facet_integrals():
            self.classes[i] = extract_classes(i._integrand)
        for i in form.interior_facet_integrals():
            self.classes[i] = extract_classes(i._integrand)

    def __str__(self):
        "Print summary of form data"

        return tstr((("Domain",                   self.domain),
                     ("Geometric dimension",      self.geometric_dimension),
                     ("Topological dimension",    self.topological_dimension),
                     ("Rank",                     self.rank),
                     ("Number of coefficients",   self.num_coefficients),
                     ("Number of cell integrals", len(self.form.cell_integrals())),
                     ("Number of e.f. integrals", len(self.form.exterior_facet_integrals())),
                     ("Number of i.f. integrals", len(self.form.interior_facet_integrals())),
                     ("Basis functions",          lstr(self.basisfunctions)),
                     ("Coefficients",             lstr(self.coefficients)),
                     ("Unique elements",          lstr(self.unique_elements))))
