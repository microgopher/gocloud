import tests 
import unittest

suite = unittest.TestLoader().loadTestsFromTestCase(
    tests.CustomerTestCase)

unittest.TextTestRunner(verbosity=2).run(suite)
