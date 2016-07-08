"""
Copyright 2016 Steven Diamond, Enzo Busseti

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

from cvxpy.atoms.atom import Atom

class ScalarAtom(Atom):
    """ Base class for scalar atoms. """

    def size_from_args(self):
        """Returns the (row, col) size of the expression.
        """
        return (1, 1)

    def index_from_args(self):
        """Returns the index and column index of the expression.
        """
        return (None, None)



