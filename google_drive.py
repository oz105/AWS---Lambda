from __future__ import print_function

import os.path
import datetime
from datetime import datetime, timedelta

from apiclient import errors
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']

# to get the date from the str date
def to_valid_date(date):
    temp_date = date[:10]
    temp_date = temp_date.split('-')
    res = datetime(int(temp_date[0]), int(temp_date[1]), int(temp_date[2])).date()

    return res


# this func get the id of the file and del it

def delete_file(service, file_id):
  try:
    service.files().delete(fileId=file_id).execute()

  except errors.HttpError as error:
    print ('An error occurred: %s' % error)


# build the service of google drive api and check the date of modified items
def main():

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        API_KEY = open("api_key.txt", "r")
        service = build('drive', 'v3', credentials=creds, developerKey=API_KEY)

        folder_id = '1pdCn_ceKtB4vptpc6by2Cog4A2UU7MOW'  # The folder of 'anipo'
        items = []
        page_token = ""
        while page_token is not None:
            response = service.files().list(q="'" + folder_id + "' in parents", pageSize=1000, pageToken=page_token,
                                            fields="nextPageToken, files(id, name, createdTime, modifiedTime)").execute()
            items.extend(response.get('files', []))
            page_token = response.get('nextPageToken')

        print(items)

        items_to_del = []
        today = datetime.now()  # get the time of today
        date_of_5_days = (today - timedelta(days=5)).date()  # get the date 5 days ago

        # add all the id of items we need to del to list
        for item in items:
            date_of_item = to_valid_date(item['modifiedTime'])
            # check if its pass 5 days
            if date_of_item <= date_of_5_days:
                items_to_del.append(item['id'])


        print(items_to_del)
        # del every item in the list from google drive.
        for item_id in items_to_del:
            delete_file(service, item_id)

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()


