import tests 
import unittest

suite = unittest.TestLoader().loadTestsFromTestCase(
    tests.ProviderTestCase)

unittest.TextTestRunner(verbosity=2).run(suite)
