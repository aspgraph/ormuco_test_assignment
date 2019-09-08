import unittest
from version_comp import compare_versions
from version_comp import CompareFormatException

# Unit tests for comparing version strings
# Order: first string, second string, result
unit_tests = \
    [['1.1', '1.2', 'Less'],
     ['2.0', '0.2', 'Greater'],
     ['8.9', '8.9', 'Equals'],
     ['0.0', '0.0', 'Equals'],
     ['1.0.1', '1.0', 'Greater'],
     ['0.569999999999999', '0.569999999999999', 'Equals'],
     ['1.999999999999999999999999', '1.999999999999999999999998', 'Greater'],
     ['232425252553.2', '2342442.63434353535', 'Greater'],
     ['9585.2', '4242424909420294024924.0', 'Less'],
     ['385938539583.1', '385938539583.1', 'Equals'],
     ['3.9', '-0.5', 'Err'],
     ['4.-0', '8.1', 'Err'],
     ['-9.-1', '4.9', 'Err'],
     ['.', '0.7', 'Err'],
     ['.', '.', 'Err'],
     ['1.', '7.8', 'Err'],
     ['.9', '0.1', 'Err'],
     ['10', '1.0', 'Greater'],
     ['1.0', '1', 'Equals'],
     ['1.1.1', '1.11', 'Less'],
     ['1.0.0.0.0', '1.0', 'Equals'],
     ['1.0.0.0.0.0.0.0.0.1', '1.0', 'Greater'],
     ['0.5a3', '0.5rc1', 'Less'],
     ['1.1rc', '0.9', 'Greater'],
     ['1.8.5b3', '1.8.5', 'Less'],
     ['6.5.1r', '6.5.2', 'Less'],
     ['rc', '0.0', 'Err'],
     ['a1', '0.1', 'Err']]


# Creating dynamic testing functions
def compare_versions_test(v1, v2, res):
    def test(self):
        try:
            self.assertEquals(res, compare_versions(v1, v2))
        except CompareFormatException:
            self.assertEquals(res, 'Err')
    return test


# TestCase derived class to add dynamic functions to
class VersionTest(unittest.TestCase):
    longMessage = True

# Unit testing program entry point
if __name__ == '__main__':
    for s1, s2, res in unit_tests:
        # Adding dynamically generated functions to the test cases
        test_name = 'comp_{0}_vs_{1}_is_{2}'.format(s1.replace('.', '_'), s2.replace('.', '_'), res)
        test_func = compare_versions_test(s1, s2, res)
        setattr(VersionTest, 'test_' + test_name, test_func)

    unittest.main()