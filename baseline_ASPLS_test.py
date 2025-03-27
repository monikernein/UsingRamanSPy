import unittest
# import pytest
import baseline_ASPLS
# from baseline_ASPLS import BaselineASPLS
from unittest.mock import patch

class TestBaselineASPLS(unittest.TestCase):

    @patch('ramanspy.load.witec')
    @patch('ramanspy.preprocessing.Pipeline.apply')
    def test_success(self, mock_load,  mock_pipeline_apply):
        test_cases = [
        ({'file_name': './TestSpectra.mat'}),
        ({'file_name': './TestImage.mat'})
        ]
        # This successfully calls the method we want to test
        # next step is to add mocking
        # assert that create pipeline is called with correct parameter
        # assert that the image generator and show are called
        for test_param in test_cases:
            thing = baseline_ASPLS.BaselineASPLS('unittest', test_param)
            thing.preprocessFile()
            # assert load file is called with file name
            assert mock_load.called_with(test_param)
            # assert pipeline apply is called
            assert mock_pipeline_apply.called
            # need to work a close window call into the show mock or the test will hang

if __name__ == '__main__':
    unittest.main()
