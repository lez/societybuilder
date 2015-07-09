#!/usr/bin/env python

from xhpy.init import register_xhpy_module

import unittest

# HACK: for Python < 2.7, monkey-patch unittest to include a stub
# implementation of unittest.skip().
try:
    unittest.skip
except AttributeError:
    def _unittest_skip(msg):
        def wrap(func):
            def wrapped_func(*args):
                pass
            return wrapped_func
        return wrap
    unittest.skip = _unittest_skip

class XHPyFullTests(unittest.TestCase):
  def test_array_constant(self):
    register_xhpy_module('array_constant')
    from . import array_constant
    self.assertEqual('pass', array_constant.result)

  def test_attr_blank(self):
    register_xhpy_module('attr_blank')
    from . import attr_blank
    self.assertEqual('pass', attr_blank.result)

  def test_attr_entity(self):
    register_xhpy_module('attr_entity')
    from . import attr_entity
    self.assertEqual('pass', attr_entity.result)

  def test_attr_float(self):
    register_xhpy_module('attr_float')
    from . import attr_float
    self.assertEqual('pass', attr_float.result)

  def test_attributes(self):
    register_xhpy_module('attributes')
    from . import attributes
    self.assertEqual('pass', attributes.result)

  def test_attributes(self):
    register_xhpy_module('attributes')
    from . import attributes
    self.assertEqual('pass', attributes.result)

  def test_class_constants(self):
    register_xhpy_module('class_constants')
    from . import class_constants
    self.assertEqual({'etc': 1, 'bar': 2}, class_constants.result)

  def test_docstrings_01(self):
    register_xhpy_module('docstrings_01')
    from . import docstrings_01
    self.assertEqual('b', docstrings_01.result)

  def test_docstrings_02(self):
    register_xhpy_module('docstrings_02')
    from . import docstrings_02
    self.assertEqual('b', docstrings_02.result)

  def test_docstrings_03(self):
    register_xhpy_module('docstrings_03')
    from . import docstrings_03
    self.assertEqual('c', docstrings_03.result)

  def test_docstrings_05(self):
    register_xhpy_module('docstrings_05')
    from . import docstrings_05
    self.assertEqual('b', docstrings_05.result)

  def test_klass(self):
    register_xhpy_module('klass')
    from . import klass
    self.assertEqual('pass', klass.result)

  @unittest.skip('TODO: match input source lines on output')
  def test_lineno_01(self):
    register_xhpy_module('lineno_01')
    from . import lineno_01
    self.assertEqual(7, lineno_01.result[1])

  @unittest.skip('TODO: add support for comment tokens within tags')
  def test_lineno_02(self):
    register_xhpy_module('lineno_02')
    from . import lineno_02
    self.assertEqual(7, lineno_02.result[1])

  def test_logical_op(self):
    register_xhpy_module('logical_op')
    from . import logical_op
    self.assertEqual(True, logical_op.result)

  def test_pep0263_01(self):
    register_xhpy_module('pep0263_01')
    from . import pep0263_01
    self.assertEqual('<p>Andr\xe9</p>', str(pep0263_01.result))

  def test_pep0263_02(self):
    register_xhpy_module('pep0263_02')
    from . import pep0263_02
    self.assertEqual('<p>Andr\xe9</p>', str(pep0263_02.result))

  def test_pep0263_03(self):
    register_xhpy_module('pep0263_03')
    from . import pep0263_03
    self.assertEqual('<p>Andr\xe9</p>', str(pep0263_03.result))

  def test_stack_balance_fail(self):
    register_xhpy_module('stack_balance_fail')
    from . import stack_balance_fail
    self.assertEqual('pass', stack_balance_fail.result)

  def test_whitespace_01(self):
    register_xhpy_module('whitespace_01')
    from . import whitespace_01
    self.assertEqual('<a><a></a>+</a>', str(whitespace_01.result))

  def test_whitespace_02(self):
    register_xhpy_module('whitespace_02')
    from . import whitespace_02
    self.assertEqual('<a>a<a></a></a>', str(whitespace_02.result))

  def test_whitespace_03(self):
    register_xhpy_module('whitespace_03')
    from . import whitespace_03
    self.assertEqual('<a>a</a>', str(whitespace_03.result))

  def test_whitespace_04(self):
    register_xhpy_module('whitespace_04')
    from . import whitespace_04
    self.assertEqual('<a><a></a>a</a>', str(whitespace_04.result))

  def test_whitespace_05(self):
    register_xhpy_module('whitespace_05')
    from . import whitespace_05
    self.assertEqual('<a>foo</a>', str(whitespace_05.result))

  def test_whitespace_06(self):
    register_xhpy_module('whitespace_06')
    from . import whitespace_06
    self.assertEqual('<a>abc</a>', str(whitespace_06.result))

  def test_whitespace_07(self):
    register_xhpy_module('whitespace_07')
    from . import whitespace_07
    self.assertEqual('<a>abc</a>', str(whitespace_07.result))

  def test_xhpy_function_param(self):
    register_xhpy_module('xhpy_function_param')
    from . import xhpy_function_param
    self.assertEqual('pass', xhpy_function_param.result)

if __name__ == '__main__':
  unittest.main()
