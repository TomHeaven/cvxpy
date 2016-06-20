"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

from ... import settings as s
from ... import utilities as u
from ..leaf import Leaf
import cvxpy.lin_ops.lin_utils as lu
import scipy.sparse as sp
import pandas as pd ## TODO do optional import

class Variable(Leaf):
    """ The base variable class """
    # name - unique identifier.
    # rows - variable height.
    # cols - variable width.
    # index - labels of rows
    # columns - labels of columns
    def __init__(self, rows=1, cols=1, index=None, columns=None, name=None):
        self._rows = rows
        self._cols = cols
        self._index = index
        self._columns = columns
        if index is not None:
            self._rows = len(index)
            self._index = pd.Index(index)
        if columns is not None:
            if self.index is None:
                raise SyntaxError("Variables with columns must have index.")
            self._cols = len(columns)
            self._columns = pd.Index(columns)
        self.id = lu.get_id()
        if name is None:
            self._name = "%s%d" % (s.VAR_PREFIX, self.id)
        else:
            self._name = name
        self.primal_value = None
        super(Variable, self).__init__()

    def is_positive(self):
        """Is the expression positive?
        """
        return False

    def is_negative(self):
        """Is the expression negative?
        """
        return False

    @property
    def size(self):
        """Returns the (row, col) dimensions of the expression.
        """
        return (self._rows, self._cols)

    @property
    def index(self):
        """Returns the index of the expression (or None).
        """
        return self._index

    @property
    def columns(self):
        """Returns the column index of the expression (or None).
        """
        return self._columns

    def get_data(self):
        """Returns info needed to reconstruct the expression besides the args.
        """
        return [self._rows, self._cols, self.index, self.columns, self._name]

    def name(self):
        return self._name

    def save_value(self, value):
        """Save the value of the primal variable.
        """
        self.primal_value = value

    def as_series(self):
        """Returns representation of the variable as pandas Series.
        """
        if self.index is None:
            raise SyntaxError("Variable has no index")
        if self.columns is not None:
            raise SyntaxError("Variable has columns, use as_dataframe()")
        return pd.Series(index=self.index, data=self.value)

    def as_dataframe(self):
        """Returns representation of the variable as pandas DataFrame.
        """
        if self.columns is None:
            raise SyntaxError("Variable has no column index.")
        return pd.DataFrame(index=self.index, 
            columns=self.columns, data=self.value)

    @property
    def value(self):
        return self.primal_value

    @value.setter
    def value(self, val):
        """Assign a value to the variable.
        """
        val = self._validate_value(val)
        self.save_value(val)

    @property
    def grad(self):
        """Gives the (sub/super)gradient of the expression w.r.t. each variable.

        Matrix expressions are vectorized, so the gradient is a matrix.

        Returns:
            A map of variable to SciPy CSC sparse matrix or None.
        """
        return {self: sp.eye(self.size[0]*self.size[1]).tocsc()}

    def variables(self):
        """Returns itself as a variable.
        """
        return [self]

    def canonicalize(self):
        """Returns the graph implementation of the object.

        Returns:
            A tuple of (affine expression, [constraints]).
        """
        obj = lu.create_var(self.size, self.id)
        return (obj, [])

    def __repr__(self):
        """String to recreate the object.
        """
        ## TODO if we use this format, propagate to subclasses of Variable
        return "Variable%s" % self._repr_index()
