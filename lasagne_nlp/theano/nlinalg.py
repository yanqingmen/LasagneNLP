from __future__ import print_function

__author__ = 'max'

import numpy

import theano
from theano.gof import Op, Apply
from theano.tensor.nlinalg import matrix_inverse


class LogAbsDet(Op):
    """
    Computes the logarithm of absolute determinant of a square
    matrix M, log(abs(det(M))), on CPU. Avoids det(M) overflow/
    underflow.

    TODO: add GPU code!
    """

    def make_node(self, x):
        x = theano.tensor.as_tensor_variable(x)
        o = theano.tensor.scalar(dtype=x.dtype)
        return Apply(self, [x], [o])

    def perform(self, node, inputs, outputs, params=None):
        try:
            (x,) = inputs
            (z,) = outputs
            s = numpy.linalg.svd(x, compute_uv=False)
            log_abs_det = numpy.sum(numpy.log(numpy.abs(s)))
            z[0] = numpy.asarray(log_abs_det, dtype=x.dtype)
        except Exception:
            print('Failed to compute logabsdet of {}.'.format(x))
            raise

    def grad(self, inputs, g_outputs):
        [gz] = g_outputs
        [x] = inputs
        return [gz * matrix_inverse(x).T]

    def __str__(self):
        return "LogAbsDet"


logabsdet = LogAbsDet()