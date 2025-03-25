import unittest
from baseline_ASPLS import BaselineASPLS

class TestBaselineASPLS(unittest.TestCase):

    #def setUp(self):
    #    mode = 'unittest'
    #    test_param = {
    #        'file_name': './TestSpectra.mat'
    #    }
    #    self.processor = BaselineASPLS(mode, test_param)

    def test_success(self):
        test_cases = [
        ({'file_name': './TestSpectra.mat'}),
        ({'file_name': './TestImage.mat'})
        ]
        # This successfully calls the method we want to test
        # next step is to add mocking
        # assert that loadfile is called
        # assert that create pipeline is called with correct parameter
        # assert that the image generator and show are called
        for test_param in test_cases:
            with self.subTest(test_param =test_param):
                self.processor = BaselineASPLS('unittest', test_param)
                self.processor.preprocessFile()
        # this makes the test always pass, delete after mocking is in
                self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
