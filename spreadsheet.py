#!/usr/bin/env python3

# adapted from
# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html

from os import environ as env
from json import loads as parse_json
from os.path import exists as file_exists

from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_keyfile_dict():
    # get client secrets from either the environment or from a local file
    if 'client_secrets_json' in env:
        return parse_json(env['client_secrets_json'])
    elif file_exists('client_secrets.json'):
        with open('client_secrets.json') as fd:
            return parse_json(fd.read())
    raise RuntimeError('cannot find client secrets json')

def create_client():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(get_keyfile_dict(), scope)
    return gspread.authorize(creds)

app = Flask(__name__)

@app.route('/')
def index():
    client = create_client()

    # Find a workbook by id. For example, if the URL is
    #
    # https://docs.google.com/spreadsheets/d/1sbP8s0p0I0QG329lG_2uIcyb6hwcA1ZhiJrb4wMFI4o/edit#gid=0
    #
    # then you would use:
    #
    # client.open_by_key('1sbP8s0p0I0QG329lG_2uIcyb6hwcA1ZhiJrb4wMFI4o')
    workbook = client.open_by_key('1sbP8s0p0I0QG329lG_2uIcyb6hwcA1ZhiJrb4wMFI4o')

    # open the first sheet from the workbook
    sheet = workbook.get_worksheet(0)

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    return str(list_of_hashes)

if __name__ == '__main__':
    app.run(debug=True)
