#!/usr/bin/env python3

# adapted from
# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html

from os import environ as env
from json import loads as parse_json

from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_keyfile_dict():
    return parse_json(env['client_secrets_json'])

def create_client():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(get_keyfile_dict(), scope)
    return gspread.authorize(creds)

app = Flask(__name__)

@app.route('/')
def index():
    return get_keyfile_dict()
    client = create_client()

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open('Example Spreadsheet').sheet1

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    return str(list_of_hashes)

if __name__ == '__main__':
    app.run(debug=True)
