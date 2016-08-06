"""
Copyright 2016 Enzo Busseti & Steven Diamond

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

import cvxpy as cvx
from cvxpy.tests.base_test import BaseTest
import sys


class TestNoPandas(BaseTest):
    def test_missing_pandas(self):
        """Test that missing pandas is handled gracefully."""
        try:
            import pandas as pd
            if sys.version_info < (3, 3):
                return  # no easy way to do it on python2 if pandas present
        except ImportError:
            pass
        if sys.version_info >= (3, 3):
            from unittest import mock
            with mock.patch.dict('sys.modules', {'pandas': None}):
                return self._test_missing_pandas()
        else:
            return self._test_missing_pandas()

    def _test_missing_pandas(self):
        with self.assertRaises(ImportError):
            x = cvx.Variable(rows=[1,2,3], cols=range(3))
        with self.assertRaises(ImportError):
            x = cvx.Parameter(rows=range(3), cols=[1,2,3])
        with self.assertRaises(ImportError):
            x = cvx.Parameter(rows=2, cols=[1,2,3])
        x = cvx.Variable(10,10)
        with self.assertRaises(SyntaxError):
            y = x.as_series()
        with self.assertRaises(SyntaxError):
            y = x.as_dataframe()


class TestLeaves(BaseTest):

    def setUp(self):
        try:
            import pandas as pd
            self.pandas_present = True
        except ImportError:
            self.pandas_present = False
            return
        self.times = pd.date_range("2015-01-01", "2015-01-30")
        self.labels = ['aaa', 'bbb', 'ccc']
        self.range_num = range(10)

        self.x = cvx.Variable(self.times, self.labels)
        self.y = cvx.Variable(self.labels)
        self.z = cvx.Variable(self.times, 2)

        self.a = cvx.Parameter(self.times, self.range_num)
        self.b = cvx.Parameter(3, self.range_num)

        self.c = pd.Series(index = self.labels, data = 0.)
        self.D = pd.DataFrame(index = self.range_num, columns = self.times, data = 1.)

        self.c_const = cvx.Constant(self.c)
        self.D_const = cvx.Constant(self.D)

    def test_variables_basic(self):
        """Test intialization of variables indexed by pandas."""
        if not self.pandas_present:
            return
        import pandas as pd
        self.assert_(self.x.index.equals(self.times))
        self.assert_(self.x.columns.equals(pd.Index(self.labels)))
        self.assert_(self.y.index.equals(pd.Index(self.labels)))
        self.assertIs(self.y.columns, None)
        self.assert_(self.z.index.equals(self.times))
        self.assertIs(self.z.columns, None)

    def test_parameters_basic(self):
        """Test intialization of parameters indexed by pandas."""
        if not self.pandas_present:
            return
        import pandas as pd
        self.assert_(self.a.index.equals(self.times))
        self.assert_(self.a.columns.equals(pd.Index(self.range_num)))
        self.assert_(self.b.columns.equals(pd.Index(self.range_num)))
        self.assertIs(self.b.index, None)

    def test_constants_basic(self):
        """Test intialization of constants indexed by pandas."""
        if not self.pandas_present:
            return
        import pandas as pd
        self.assertIs(self.c_const.columns, None)
        self.assert_(self.c_const.index.equals(pd.Index(self.labels)))
        self.assert_(self.D_const.index.equals(pd.Index(self.range_num)))
        self.assert_(self.D_const.columns.equals(self.times))





