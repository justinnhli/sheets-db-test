#!/usr/bin/env python3

# adapted from
# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html

from json import loads as parse_json
from os import environ as env
from os.path import exists as file_exists, join as join_path, realpath, expanduser, dirname

from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials

CLIENT_SECRET_FILE = join_path(realpath(expanduser(dirname(__file__))), 'client_secret.json')

def get_keyfile_dict():
    # get client secret from either the environment or from a local file
    if 'client_secret_json' in env:
        return parse_json(env['client_secret_json'])
    elif file_exists(CLIENT_SECRET_FILE):
        with open(CLIENT_SECRET_FILE) as fd:
            return parse_json(fd.read())
    raise RuntimeError('cannot find client secret json file')

def create_client():
    # use credentials to create a client to interact with the Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(get_keyfile_dict(), scope)
    return gspread.authorize(creds)

app = Flask(__name__)

@app.route('/')
def index():
    client = create_client()

    # find a workbook by id. For example, if the URL is
    #
    # https://docs.google.com/spreadsheets/d/1sbP8s0p0I0QG329lG_2uIcyb6hwcA1ZhiJrb4wMFI4o/edit#gid=0
    #
    # then you would use:
    #
    # client.open_by_key('1sbP8s0p0I0QG329lG_2uIcyb6hwcA1ZhiJrb4wMFI4o')
    workbook = client.open_by_key('1sbP8s0p0I0QG329lG_2uIcyb6hwcA1ZhiJrb4wMFI4o')

    # open the first sheet from the workbook
    sheet = workbook.get_worksheet(0)

    # extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    return str(list_of_hashes)

if __name__ == '__main__':
    app.run(debug=True)
