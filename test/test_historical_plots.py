"""
File: test_currency.py
Author: jfmcdavi
Date: November 19th 2024
Description: File Includes Tests for Historical Trend plots

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import os
import datetime
import unittest
from unittest import mock
from currency import get_historical_trend


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCurrency(unittest.TestCase):
    """ Unit Test Setup """

    def test_one_year_jpn(self):
        """ Test for One year of Data for JPN """
        # Set up a datetime to test it off of 
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="JPY", years=1, test_end=test_end)
        assert len(output) == 12
        assert output['EXJPUS']['2024-06-01'] == 157.8600
        assert output['EXJPUS']['2024-01-01'] == 146.2943

        # Value that's not in there
        assert output['EXJPUS'].get('2023-10-01', None) is None


    def test_two_year_jpn(self):
        """ Test for Two years of Data for JPN """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="JPY", years=2, test_end=test_end)
        assert len(output) == 24

        assert output['EXJPUS']['2024-06-01'] == 157.8600
        assert output['EXJPUS']['2024-01-01'] == 146.2943

        assert output['EXJPUS']['2023-06-01'] == 141.3581
        assert output['EXJPUS']['2023-01-01'] == 130.4475

        # Value that's not in there
        assert output['EXJPUS'].get('2022-10-01', None) is None

    def test_three_year_jpn(self):
        """ Test for Three years of Data for JPN """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="JPY", years=3, test_end=test_end)
        assert len(output) == 36
        
        assert output['EXJPUS']['2024-06-01'] == 157.8600
        assert output['EXJPUS']['2024-01-01'] == 146.2943

        assert output['EXJPUS']['2023-06-01'] == 141.3581
        assert output['EXJPUS']['2023-01-01'] == 130.4475

        assert output['EXJPUS']['2022-06-01'] == 133.9619
        assert output['EXJPUS']['2022-01-01'] == 114.8255

        # Value that's not in there
        assert output['EXJPUS'].get('2021-10-01', None) is None



    def test_four_year_jpn(self):
        """ Test for 4 years of Data for JPN """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="JPY", years=4, test_end=test_end)
        assert len(output) == 48
        assert output['EXJPUS']['2024-06-01'] == 157.8600
        assert output['EXJPUS']['2024-01-01'] == 146.2943

        assert output['EXJPUS']['2023-06-01'] == 141.3581
        assert output['EXJPUS']['2023-01-01'] == 130.4475

        assert output['EXJPUS']['2022-06-01'] == 133.9619
        assert output['EXJPUS']['2022-01-01'] == 114.8255

        assert output['EXJPUS']['2021-06-01'] == 110.1073
        assert output['EXJPUS']['2021-01-01'] == 103.7883

        # Value that's not in there
        assert output['EXJPUS'].get('2020-10-01', None) is None

    def test_five_year_jpn(self):
        """ Test for 5 years of Data for JPN """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="JPY", years=5, test_end=test_end)
        assert len(output) == 60
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

        # Value that's not in there
        assert output['EXJPUS'].get('2019-10-01', None) is None

    def test_one_year_inr(self):
        """ Test for One year of Data for INR """
        # Set up a datetime to test it off of 
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="INR", years=1, test_end=test_end)
        assert len(output) == 12
        assert output['EXINUS']['2024-06-01'] == 83.46
        assert output['EXINUS']['2024-01-01'] == 83.1119

        # Value that's not in there
        assert output['EXINUS'].get('2023-10-01', None) is None

    def test_two_year_inr(self):
        """ Test for 2 years of Data for INR """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="INR", years=2, test_end=test_end)
        assert len(output) == 24

        assert output['EXINUS']['2024-06-01'] == 83.46
        assert output['EXINUS']['2024-01-01'] == 83.1119

        assert output['EXINUS']['2023-06-01'] == 82.2252
        assert output['EXINUS']['2023-01-01'] == 81.741

        # Value that's not in there
        assert output['EXINUS'].get('2022-10-01', None) is None

    def test_three_year_inr(self):
        '""" Test for 3 years of Data for INR """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="INR", years=3, test_end=test_end)
        assert len(output) == 36
        
        assert output['EXINUS']['2024-06-01'] == 83.46
        assert output['EXINUS']['2024-01-01'] == 83.1119

        assert output['EXINUS']['2023-06-01'] == 82.2252
        assert output['EXINUS']['2023-01-01'] == 81.741

        assert output['EXINUS']['2022-06-01'] == 78.09
        assert output['EXINUS']['2022-01-01'] == 74.4075

        # Value that's not in there
        assert output['EXINUS'].get('2021-10-01', None) is None


    def test_four_year_inr(self):
        """ Test for 4 years of Data for INR """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="INR", years=4, test_end=test_end)
        assert len(output) == 48
        assert output['EXINUS']['2024-06-01'] == 83.46
        assert output['EXINUS']['2024-01-01'] == 83.1119

        assert output['EXINUS']['2023-06-01'] == 82.2252
        assert output['EXINUS']['2023-01-01'] == 81.741

        assert output['EXINUS']['2022-06-01'] == 78.09
        assert output['EXINUS']['2022-01-01'] == 74.4075

        assert output['EXINUS']['2021-06-01'] == 73.5782
        assert output['EXINUS']['2021-01-01'] == 73.1106

        # Value that's not in there
        assert output['EXINUS'].get('2020-10-01', None) is None

    def test_five_year_inr(self):
        """ Test for 5 years of Data for INR """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="INR", years=5, test_end=test_end)
        assert len(output) == 60
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

        # Value that's not in there
        assert output['EXINUS'].get('2019-10-01', None) is None

    def test_six_year_cad(self):
        """ Test for 6 years of Data for CAD """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="CAD", years=6, test_end=test_end)
        len(output) == 72

        assert output['EXCAUS']['2023-12-01'] == 1.3416
        assert output['EXCAUS']['2022-12-01'] == 1.3585
        assert output['EXCAUS']['2021-12-01'] == 1.28
        assert output['EXCAUS']['2020-12-01'] == 1.2809
        assert output['EXCAUS']['2019-12-01'] == 1.3169
        assert output['EXCAUS']['2018-12-01'] == 1.3436

        # Value that's not in there
        assert output['EXCAUS'].get('2017-10-01', None) is None

    def test_seven_year_cad(self):
        """ Test for 7 years of Data for CAD """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="CAD", years=7, test_end=test_end)
        len(output) == 84

        assert output['EXCAUS']['2023-12-01'] == 1.3416
        assert output['EXCAUS']['2022-12-01'] == 1.3585
        assert output['EXCAUS']['2021-12-01'] == 1.28
        assert output['EXCAUS']['2020-12-01'] == 1.2809
        assert output['EXCAUS']['2019-12-01'] == 1.3169
        assert output['EXCAUS']['2018-12-01'] == 1.3436
        assert output['EXCAUS']['2017-12-01'] == 1.2769

        # Value that's not in there
        assert output['EXCAUS'].get('2016-10-01', None) is None

    def test_eight_year_cad(self):
        """ Test for 8 years of Data for CAD """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="CAD", years=8, test_end=test_end)
        len(output) == 96

        assert output['EXCAUS']['2023-12-01'] == 1.3416
        assert output['EXCAUS']['2022-12-01'] == 1.3585
        assert output['EXCAUS']['2021-12-01'] == 1.28
        assert output['EXCAUS']['2020-12-01'] == 1.2809
        assert output['EXCAUS']['2019-12-01'] == 1.3169
        assert output['EXCAUS']['2018-12-01'] == 1.3436
        assert output['EXCAUS']['2017-12-01'] == 1.2769
        assert output['EXCAUS']['2016-12-01'] == 1.3339

        # Value that's not in there
        assert output['EXCAUS'].get('2015-10-01', None) is None

    def test_nine_year_cad(self):
        """ Test for 9 years of Data for CAD """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="CAD", years=9, test_end=test_end)
        len(output) == 108

        assert output['EXCAUS']['2023-12-01'] == 1.3416
        assert output['EXCAUS']['2022-12-01'] == 1.3585
        assert output['EXCAUS']['2021-12-01'] == 1.28
        assert output['EXCAUS']['2020-12-01'] == 1.2809
        assert output['EXCAUS']['2019-12-01'] == 1.3169
        assert output['EXCAUS']['2018-12-01'] == 1.3436
        assert output['EXCAUS']['2017-12-01'] == 1.2769
        assert output['EXCAUS']['2016-12-01'] == 1.3339
        assert output['EXCAUS']['2015-12-01'] == 1.3713

        # Value that's not in there
        assert output['EXCAUS'].get('2014-10-01', None) is None
    
    def test_ten_year_cad(self):
        """ Test for 10 years of Data for CAD """
        test_end = datetime.datetime(2024, 11, 1)
        output = get_historical_trend(base_currency="CAD", years=10, test_end=test_end)
        len(output) == 120

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

        # Value that's not in there
        assert output['EXCAUS'].get('2013-10-01', None) is None
        
    def test_bad_inputs(self):
        """ Bad Input Test """
        assert get_historical_trend(base_currency="FAKE", years=2) is None
        assert get_historical_trend(base_currency="JPN", years="two") is None
        assert get_historical_trend(base_currency="JPN", years=0) is None
        assert get_historical_trend(base_currency="JPN", years=11) is None

if __name__ == '__main__':
    unittest.main()