#!/usr/bin/env python3

__author__ = "j3p0uk"

import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Sheets(object):
    """
    Encapsulate interactions with Google Sheets
    """
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.values = None

    # Override magic functions to make this object indexable into the sheet values

    def get_creds(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        pickle_location = 'token.pickle'
        if os.path.exists(pickle_location):
            with open(pickle_location, 'rb') as token:
                creds = pickle.load(token)
                print("Loaded token from: {}".format(pickle_location))
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(pickle_location, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def read_sheet(self, sheet_id, data_range):
        self.service = build('sheets', 'v4', credentials=self.get_creds())

        # Call the Sheets API
        self.sheet = self.service.spreadsheets()
        self.result = self.sheet.values().get(spreadsheetId=sheet_id, range=data_range,
                                              valueRenderOption='FORMULA').execute()
        self.values = self.result.get('values', [])

        if not self.values:
            print('No data found.')
        else:
            print('Found {} rows of data'.format(len(self.values)))

    def get_values(self, sheet=None, data_range=None):
        if sheet is None:
            sheet = os.environ.get('SHEET')
        if data_range is None:
            data_range = os.environ.get('DATA_RANGE')

        if sheet is None or data_range is None:
            print("Need both SHEET {} and DATA_RANGE {} to get values".format(sheet, data_range))
            self.values = None
        else:
            if self.values is None:
                self.read_sheet(sheet, data_range)
        return self.values
