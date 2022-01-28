'''
Save and load bed status information
'''

import json

FILE_NAME = 'status.json'

# open status file
def get():
    try:
        with open(FILE_NAME, 'r') as file:
            data = json.load(file)
            file.close()

            return data
    except Exception as e:
        print('ERROR: Getting from ' + FILE_NAME, e)


# save/update status file
def save(updated_data):
    try:
        status = get()

        for key, value in updated_data.items():
            status[key] = value

        with open(FILE_NAME, 'w') as file:
            json.dump(status, file)
            file.close()

    except Exception as e:
        print('ERROR: Saving status to ' + FILE_NAME, e)
