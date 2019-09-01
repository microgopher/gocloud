import tests 
import unittest

suite = unittest.TestLoader().loadTestsFromTestCase(
    tests.AuthenticationTestCase)
#suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
#    test_bucketlist.BucketListTestCase))
#suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
#    test_bucketlist_items.BucketListItemTestCase))

unittest.TextTestRunner(verbosity=2).run(suite)
