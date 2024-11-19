import sys
import os
import datetime
import unittest
from unittest import mock
from currency import get_historical_trend


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCurrency(unittest.TestCase):

    def test_one_year_jpn(self):
        # Set up a datetime to test it off of 
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="JPY", years=1, test_end=test_end)
        assert len(output) == 11
        assert output['EXJPUS']['2024-06-01'] == 157.8600
        assert output['EXJPUS']['2024-01-01'] == 146.2943

    def test_two_year_jpn(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="JPY", years=2, test_end=test_end)
        assert len(output) == 23

        assert output['EXJPUS']['2024-06-01'] == 157.8600
        assert output['EXJPUS']['2024-01-01'] == 146.2943

        assert output['EXJPUS']['2023-06-01'] == 141.3581
        assert output['EXJPUS']['2023-01-01'] == 130.4475

    def test_three_year_jpn(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="JPY", years=3, test_end=test_end)
        assert len(output) == 35
        
        assert output['EXJPUS']['2024-06-01'] == 157.8600
        assert output['EXJPUS']['2024-01-01'] == 146.2943

        assert output['EXJPUS']['2023-06-01'] == 141.3581
        assert output['EXJPUS']['2023-01-01'] == 130.4475

        assert output['EXJPUS']['2022-06-01'] == 133.9619
        assert output['EXJPUS']['2022-01-01'] == 114.8255



    def test_four_year_jpn(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="JPY", years=4, test_end=test_end)
        assert len(output) == 47
        assert output['EXJPUS']['2024-06-01'] == 157.8600
        assert output['EXJPUS']['2024-01-01'] == 146.2943

        assert output['EXJPUS']['2023-06-01'] == 141.3581
        assert output['EXJPUS']['2023-01-01'] == 130.4475

        assert output['EXJPUS']['2022-06-01'] == 133.9619
        assert output['EXJPUS']['2022-01-01'] == 114.8255

        assert output['EXJPUS']['2021-06-01'] == 110.1073
        assert output['EXJPUS']['2021-01-01'] == 103.7883

    def test_five_year_jpn(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="JPY", years=5, test_end=test_end)
        assert len(output) == 59
        assert output['EXJPUS']['2024-06-01'] == 157.8600
        assert output['EXJPUS']['2024-01-01'] == 146.2943

        assert output['EXJPUS']['2023-06-01'] == 141.3581
        assert output['EXJPUS']['2023-01-01'] == 130.4475

        assert output['EXJPUS']['2022-06-01'] == 133.9619
        assert output['EXJPUS']['2022-01-01'] == 114.8255

        assert output['EXJPUS']['2021-06-01'] == 110.1073
        assert output['EXJPUS']['2021-01-01'] == 103.7883

        assert output['EXJPUS']['2020-06-01'] == 107.5782
        assert output['EXJPUS']['2020-01-01'] == 109.2667



if __name__ == '__main__':
    unittest.main()