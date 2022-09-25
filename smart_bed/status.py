'''
Save and load bed status information
'''

import json
import os
import sys

FILE_NAME = 'status.json'
DIR_PATH = os.path.dirname(sys.modules['__main__'].__file__)

if len(DIR_PATH) > 0:
    FILE_NAME = DIR_PATH + '/' + FILE_NAME


# open status file
def get():
    try:
        with open(FILE_NAME, 'r') as file:
            data = json.load(file)
            file.close()

            return data
    except Exception as error:
        print('ERROR: Getting from ' + FILE_NAME, error)


# save/update status file
def save(updated_data):
    try:
        status = get()

        for key, value in updated_data.items():
            status[key] = value

        with open(FILE_NAME, 'w') as file:
            json.dump(status, file)
            file.close()

    except Exception as error:
        print('ERROR: Saving status to ' + FILE_NAME, error)
