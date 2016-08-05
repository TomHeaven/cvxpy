"""
Copyright 2016 Enzo Busseti and Steven Diamond

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

def sum_indexes(indexs_columns):
    """Give the indexes resulting from summing a list of indexes.

    Args:
        shapes: A list of (index, columns) tuples.

    If one variable has the right size, but misses index or columns,
    we accept it. If two variables have a index or columns, we require
    that they are the same.

    Returns:
        The (index, columns) of the sum. 
    """
    indexes = [el[0] for el in indexs_columns if el[0] is not None]
    columns = [el[1] for el in indexs_columns if el[1] is not None]
    for index in indexes:
        if not index.equals(indexes[0]):
            raise ValueError(
                "Incompatible indexes")
    for column in columns:
        if not column.equals(columns[0]):
            raise ValueError(
                "Incompatible column indexes")
    # TODO implement dynamic reindexing
    return (None if len(indexes) == 0 else indexes[0], 
            None if len(columns) == 0 else columns[0])

def mul_indexes(lh_indexes, rh_indexes):
    """Give the columns and row index resulting from multiplying
    two column and row indexes.

    Args:
        lh_indexes: A (index, column index) tuple.
        rh_indexes: A (index, column index) tuple.

    Returns:
        The index (index, column index) of the product.
    """
    if lh_indexes[0] is None and lh_indexes[1] is None:
        return rh_indexes
    elif rh_indexes[0] is None and rh_indexes[1] is None:
        return lh_indexes
    else: # TODO implement dynamic reindexing
        if lh_shape[1] != rh_shape[0]:
            raise ValueError("Incompatible dimensions %s %s" % (
                lh_shape, rh_shape))
        return (lh_shape[0], rh_shape[1])
