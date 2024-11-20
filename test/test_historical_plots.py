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

    def test_one_year_inr(self):
        # Set up a datetime to test it off of 
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="INR", years=1, test_end=test_end)
        assert len(output) == 11
        assert output['EXINUS']['2024-06-01'] == 83.46
        assert output['EXINUS']['2024-01-01'] == 83.1119

    def test_two_year_inr(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="INR", years=2, test_end=test_end)
        assert len(output) == 23

        assert output['EXINUS']['2024-06-01'] == 83.46
        assert output['EXINUS']['2024-01-01'] == 83.1119

        assert output['EXINUS']['2023-06-01'] == 82.2252
        assert output['EXINUS']['2023-01-01'] == 81.741

    def test_three_year_inr(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="INR", years=3, test_end=test_end)
        assert len(output) == 35
        
        assert output['EXINUS']['2024-06-01'] == 83.46
        assert output['EXINUS']['2024-01-01'] == 83.1119

        assert output['EXINUS']['2023-06-01'] == 82.2252
        assert output['EXINUS']['2023-01-01'] == 81.741

        assert output['EXINUS']['2022-06-01'] == 78.09
        assert output['EXINUS']['2022-01-01'] == 74.4075



    def test_four_year_inr(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="INR", years=4, test_end=test_end)
        assert len(output) == 47
        assert output['EXINUS']['2024-06-01'] == 83.46
        assert output['EXINUS']['2024-01-01'] == 83.1119

        assert output['EXINUS']['2023-06-01'] == 82.2252
        assert output['EXINUS']['2023-01-01'] == 81.741

        assert output['EXINUS']['2022-06-01'] == 78.09
        assert output['EXINUS']['2022-01-01'] == 74.4075

        assert output['EXINUS']['2021-06-01'] == 73.5782
        assert output['EXINUS']['2021-01-01'] == 73.1106

    def test_five_year_inr(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="INR", years=5, test_end=test_end)
        assert len(output) == 59
        assert output['EXINUS']['2024-06-01'] == 83.46
        assert output['EXINUS']['2024-01-01'] == 83.1119

        assert output['EXINUS']['2023-06-01'] == 82.2252
        assert output['EXINUS']['2023-01-01'] == 81.741

        assert output['EXINUS']['2022-06-01'] == 78.09
        assert output['EXINUS']['2022-01-01'] == 74.4075

        assert output['EXINUS']['2021-06-01'] == 73.5782
        assert output['EXINUS']['2021-01-01'] == 73.1106

        assert output['EXINUS']['2020-06-01'] == 75.7077
        assert output['EXINUS']['2020-01-01'] == 71.279

    def test_six_year_cad(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="CAD", years=6, test_end=test_end)
        len(output) == 71

        assert output['EXCAUS']['2023-12-01'] == 1.3416
        assert output['EXCAUS']['2022-12-01'] == 1.3585
        assert output['EXCAUS']['2021-12-01'] == 1.28
        assert output['EXCAUS']['2020-12-01'] == 1.2809
        assert output['EXCAUS']['2019-12-01'] == 1.3169
        assert output['EXCAUS']['2018-12-01'] == 1.3436
        


    def test_seven_year_cad(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="CAD", years=7, test_end=test_end)
        len(output) == 83

        assert output['EXCAUS']['2023-12-01'] == 1.3416
        assert output['EXCAUS']['2022-12-01'] == 1.3585
        assert output['EXCAUS']['2021-12-01'] == 1.28
        assert output['EXCAUS']['2020-12-01'] == 1.2809
        assert output['EXCAUS']['2019-12-01'] == 1.3169
        assert output['EXCAUS']['2018-12-01'] == 1.3436
        assert output['EXCAUS']['2017-12-01'] == 1.2769

    def test_eight_year_cad(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="CAD", years=8, test_end=test_end)
        len(output) == 95

        assert output['EXCAUS']['2023-12-01'] == 1.3416
        assert output['EXCAUS']['2022-12-01'] == 1.3585
        assert output['EXCAUS']['2021-12-01'] == 1.28
        assert output['EXCAUS']['2020-12-01'] == 1.2809
        assert output['EXCAUS']['2019-12-01'] == 1.3169
        assert output['EXCAUS']['2018-12-01'] == 1.3436
        assert output['EXCAUS']['2017-12-01'] == 1.2769
        assert output['EXCAUS']['2016-12-01'] == 1.3339

    def test_nine_year_cad(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="CAD", years=9, test_end=test_end)
        len(output) == 107

        assert output['EXCAUS']['2023-12-01'] == 1.3416
        assert output['EXCAUS']['2022-12-01'] == 1.3585
        assert output['EXCAUS']['2021-12-01'] == 1.28
        assert output['EXCAUS']['2020-12-01'] == 1.2809
        assert output['EXCAUS']['2019-12-01'] == 1.3169
        assert output['EXCAUS']['2018-12-01'] == 1.3436
        assert output['EXCAUS']['2017-12-01'] == 1.2769
        assert output['EXCAUS']['2016-12-01'] == 1.3339
        assert output['EXCAUS']['2015-12-01'] == 1.3713
    
    def test_ten_year_cad(self):
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="CAD", years=10, test_end=test_end)
        len(output) == 119

        assert output['EXCAUS']['2023-12-01'] == 1.3416
        assert output['EXCAUS']['2022-12-01'] == 1.3585
        assert output['EXCAUS']['2021-12-01'] == 1.28
        assert output['EXCAUS']['2020-12-01'] == 1.2809
        assert output['EXCAUS']['2019-12-01'] == 1.3169
        assert output['EXCAUS']['2018-12-01'] == 1.3436
        assert output['EXCAUS']['2017-12-01'] == 1.2769
        assert output['EXCAUS']['2016-12-01'] == 1.3339
        assert output['EXCAUS']['2015-12-01'] == 1.3713
        assert output['EXCAUS']['2014-12-01'] == 1.1532
        
    def test_bad_inputs(self):
        assert get_historical_trend(base_currency="FAKE", years=2) is None
        assert get_historical_trend(base_currency="JPN", years="two") is None
        assert get_historical_trend(base_currency="JPN", years=0) is None
        assert get_historical_trend(base_currency="JPN", years=11) is None

if __name__ == '__main__':
    unittest.main()