import tests 
import unittest

suite = unittest.TestLoader().loadTestsFromTestCase(
    tests.ACLTestCase)

unittest.TextTestRunner(verbosity=2).run(suite)
