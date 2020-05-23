#!/usr/bin/env python

__author__ = "j3p0uk"

import io
import net_uml_draw
import nose.tools
import unittest

FAKE_VALUES = [["header"], ["data"]]


class TestNetUMLDrawSheets(object):
    def __init__(self):
        self.sheets = net_uml_draw.sheets.Sheets()

    def test_get_creds_flow(self):
        creds = None
        with unittest.mock.patch('os.path.exists', return_value=False) as mock_exists, \
                unittest.mock.patch('pickle.dump') as mock_pickle, \
                unittest.mock.patch('net_uml_draw.sheets.InstalledAppFlow',
                                    return_value=unittest.mock.MagicMock()) as mock_flow:
            creds = self.sheets.get_creds()
        nose.tools.ok_(mock_exists.call_count == 1)
        nose.tools.ok_(mock_pickle.call_count == 1)
        nose.tools.ok_(creds is not None)
        expected_creds_calls = [
            unittest.mock.call.from_client_secrets_file(
                'credentials.json', ['https://www.googleapis.com/auth/spreadsheets.readonly']),
            unittest.mock.call.from_client_secrets_file().run_local_server(port=0)]
        nose.tools.ok_(mock_flow.mock_calls == expected_creds_calls,
                       "Calls are {} not {}".format(mock_flow.mock_calls, expected_creds_calls))

    def test_get_creds_pickle(self):
        creds = None
        with unittest.mock.patch('os.path.exists', return_value=True) as mock_exists, \
                unittest.mock.patch('pickle.load',
                                    return_value=unittest.mock.MagicMock()) as mock_pickle, \
                unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            creds = self.sheets.get_creds()
        nose.tools.ok_(mock_exists.call_count == 1)
        nose.tools.ok_(mock_pickle.call_count == 1)
        printed = mock_stdout.getvalue().strip()
        nose.tools.ok_(printed == 'Loaded token from: token.pickle',
                       "Output was {}".format(printed))
        nose.tools.ok_(creds is not None)
        expected_creds_calls = [unittest.mock.call.__bool__(),
                                unittest.mock.call.valid.__bool__()]
        nose.tools.ok_(creds.mock_calls == expected_creds_calls,
                       "Calls are {} not {}".format(creds.mock_calls, expected_creds_calls))

    def test_get_creds_pickle_refresh(self):
        creds = None
        creds_mock = unittest.mock.MagicMock()
        creds_mock.valid = False
        with unittest.mock.patch('os.path.exists', return_value=True) as mock_exists, \
                unittest.mock.patch('pickle.load', return_value=creds_mock) as mock_load, \
                unittest.mock.patch('pickle.dump') as mock_dump, \
                unittest.mock.patch('net_uml_draw.sheets.Request',
                                    return_value='request') as mock_request, \
                unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            creds = self.sheets.get_creds()
        nose.tools.ok_(mock_exists.call_count == 1)
        nose.tools.ok_(mock_load.call_count == 1)
        nose.tools.ok_(mock_dump.call_count == 1)
        nose.tools.ok_(mock_request.call_count == 1)
        printed = mock_stdout.getvalue().strip()
        nose.tools.ok_(printed == 'Loaded token from: token.pickle',
                       "Output was {}".format(printed))
        nose.tools.ok_(creds is not None)
        expected_creds_calls = [unittest.mock.call.__bool__(),
                                unittest.mock.call.__bool__(),
                                unittest.mock.call.expired.__bool__(),
                                unittest.mock.call.refresh_token.__bool__(),
                                unittest.mock.call.refresh('request')]
        nose.tools.ok_(creds.mock_calls == expected_creds_calls,
                       "Calls are {} not {}".format(creds.mock_calls, expected_creds_calls))

    @unittest.mock.patch.dict('os.environ', {'DATA_RANGE': 'range'})
    def test_get_values_no_data_range(self):
        values = self.sheets.get_values()
        nose.tools.ok_(values is None)

    @unittest.mock.patch.dict('os.environ', {'SHEET': "sheet"})
    def test_get_values_no_sheet(self):
        values = self.sheets.get_values()
        nose.tools.ok_(values is None)

    def read_sheet_side_effect(self, sheet, data_range):
        self.sheets.values = FAKE_VALUES

    @unittest.mock.patch.dict('os.environ', {'SHEET': "sheet", 'DATA_RANGE': 'range'})
    def test_get_values_env(self):
        self.sheets.read_sheet = unittest.mock.MagicMock()
        self.sheets.read_sheet.side_effect = self.read_sheet_side_effect
        values = self.sheets.get_values()
        nose.tools.ok_(values == FAKE_VALUES, "Values is {} not {}".format(values, FAKE_VALUES))

    def test_get_values_arg(self):
        self.sheets.read_sheet = unittest.mock.MagicMock()
        self.sheets.read_sheet.side_effect = self.read_sheet_side_effect
        values = self.sheets.get_values("sheet", "range")
        print(self.sheets.read_sheet.calls)
        nose.tools.ok_(values == FAKE_VALUES, "Values is {} not {}".format(values, FAKE_VALUES))

    def test_read_sheet(self):
        self.sheets.get_creds = unittest.mock.MagicMock()
        net_uml_draw.sheets.build = unittest.mock.MagicMock()
        service = unittest.mock.MagicMock()

        net_uml_draw.sheets.build.return_value = service
        service.spreadsheets().values().get().execute().get.return_value = FAKE_VALUES

        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.sheets.read_sheet("sheet", "range")
        printed = mock_stdout.getvalue().strip()
        nose.tools.ok_(printed == 'Found 2 rows of data', "Output was {}".format(printed))
        nose.tools.ok_(self.sheets.values == FAKE_VALUES,
                       "Values is {} not {}".format(self.sheets.values, FAKE_VALUES))

    def test_read_sheet_fail(self):
        self.sheets.get_creds = unittest.mock.MagicMock()
        net_uml_draw.sheets.build = unittest.mock.MagicMock()
        service = unittest.mock.MagicMock()

        net_uml_draw.sheets.build.return_value = service
        service.spreadsheets().values().get().execute().get.return_value = None

        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.sheets.read_sheet("sheet", "range")
        printed = mock_stdout.getvalue().strip()
        nose.tools.ok_(printed == 'No data found.', "Output was {}".format(printed))
        nose.tools.ok_(self.sheets.values is None,
                       "Values is {} not None".format(self.sheets.values))
