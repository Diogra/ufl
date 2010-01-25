"""FormData class easy for collecting of various data about a form."""

__authors__ = "Martin Sandve Alnes"
__date__ = "2008-09-13"

# Modified by Anders Logg, 2008.
# Last changed: 2010-01-25

from itertools import chain

from ufl.log import error, warning
from ufl.assertions import ufl_assert
from ufl.common import lstr, tstr, sstr, estr
from ufl.form import Form

from ufl.algorithms.preprocess import preprocess
from ufl.algorithms.analysis import extract_elements
from ufl.algorithms.analysis import extract_sub_elements
from ufl.algorithms.analysis import extract_num_sub_domains
from ufl.algorithms.analysis import extract_integral_data
from ufl.algorithms.analysis import unique_tuple

class FormData(object):
    "Class collecting various information extracted from a Form."

    def __init__(self, form, name="a", object_names={}):
        "Create form data for given form"

        # Check that we get a form
        ufl_assert(isinstance(form, Form), "Expecting Form.")

        # Preprocess form if necessary
        if not form.is_preprocessed():
            form = preprocess(form)

        # Check that form has integrals
        if not form._integrals:
            error("Unable to extract form data. Reason: Form is empty.")

        # Store data extracted by preprocessing
        self.arguments             = form._form_data[0]
        self.coefficients          = form._form_data[1]
        self.original_arguments    = form._form_data[2]
        self.original_coefficients = form._form_data[3]

        # Store name of form
        self.name = name

        # Store signature of form
        self.signature = form.signature()

        # Store some useful dimensions
        self.rank = len(self.arguments)
        self.num_coefficients = len(self.coefficients)

        # Store argument names
        self.argument_names = [object_names.get(id(self.original_arguments[i]), "v%d" % i)
                               for i in range(self.rank)]

        # Store coefficient names
        self.coefficient_names = [object_names.get(id(self.original_coefficients[i]), "w%d" % i)
                                  for i in range(self.num_coefficients)]

        # Store elements, sub elements and element map
        self.elements            = extract_elements(form)
        self.unique_elements     = unique_tuple(self.elements)
        self.sub_elements        = extract_sub_elements(self.elements)
        self.unique_sub_elements = unique_tuple(self.sub_elements)

        # Store cell
        if self.elements:
            cells = [element.cell() for element in self.elements]
            cells = [cell for cell in cells if not cell.domain() is None]
            if len(cells) == 0:
                error("Unable to extract form data. Reason: Missing cell definition in form.")
            self.cell = cells[0]
        elif form._integrals:
            # Special case to allow functionals only depending on geometric variables, with no elements
            self.cell = form._integrals[0].integrand().cell()
        else:
            # Special case to allow integral of constants to pass through without crashing
            self.cell = None
            warning("Form is empty, no elements or integrals, cell is undefined.")

        # Store data related to cell
        if self.cell is None:
            warning("No cell is defined in form.")
            self.geometric_dimension = None
            self.topological_dimension = None
            self.num_facets = None
        else:
            self.geometric_dimension = self.cell.geometric_dimension()
            self.topological_dimension = self.cell.topological_dimension()
            self.num_facets = self.cell.num_facets()

        # Store number of domains for integral types
        (self.num_cell_domains,
         self.num_exterior_facet_domains,
         self.num_interior_facet_domains,
         self.num_macro_cell_domains,
         self.num_surface_domains) = extract_num_sub_domains(form)

        # Store integrals stored by type and sub domain
        self.integral_data = extract_integral_data(form)

    def __str__(self):
        "Return formatted summary of form data"
        return tstr((("Name",                               self.name),
                     ("Rank",                               self.rank),
                     ("Cell",                               self.cell),
                     ("Topological dimension",              self.topological_dimension),
                     ("Geometric dimension",                self.geometric_dimension),
                     ("Number of facets",                   self.num_facets),
                     ("Number of coefficients",             self.num_coefficients),
                     ("Number of cell domains",             self.num_cell_domains),
                     ("Number of exterior facet domains",   self.num_exterior_facet_domains),
                     ("Number or interior facet domains",   self.num_interior_facet_domains),
                     ("Number of macro cell domains",       self.num_macro_cell_domains),
                     ("Number of surface domains",          self.num_surface_domains),
                     ("Arguments",                          lstr(self.arguments)),
                     ("Coefficients",                       lstr(self.coefficients)),
                     ("Argument names",                     lstr(self.argument_names)),
                     ("Coefficient names",                  lstr(self.coefficient_names)),
                     ("Unique elements",                    estr(self.unique_elements)),
                     ("Unique sub elements",                estr(self.unique_sub_elements))))
