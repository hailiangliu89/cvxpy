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

from cvxpy.atoms.affine.trace import trace
from cvxpy.constraints.psd import PSD
from cvxpy.expressions.variables.variable import Variable


def matrix_frac_canon(expr, args):
    X = args[0]  # n by m matrix.
    P = args[1]  # n by n matrix.
    n, m = X.shape
    # Create a matrix with Schur complement T - X.T*P^-1*X.
    M = Variable(n+m, n+m)
    T = Variable(m, m)
    constraints = []
    # Fix M using the fact that P must be affine by the DCP rules.
    # M[0:n, 0:n] == P.
    constraints.append(M[0:n, 0:n] == P)
    # M[0:n, n:n+m] == X
    constraints.append(M[0:n, n:n+m] == X)
    # M[n:n+m, n:n+m] == T
    constraints.append(M[n:n+m, n:n+m] == T)
    # Add SDP constraint.
    constraints.append(PSD(M))
    return trace(T), constraints