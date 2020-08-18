import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '10Lo6SFntXxR9VPTIsnDMMy4K0dvDRBE01MHerxT_VH8'
RANGE_NAME = 'A1:B1'


def get_inputs_from_sheet():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    return values


def message_friends():
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=/Users/christophermohammed/Library/Application Support/Google/Chrome/Default")
    driver = webdriver.Chrome(executable_path='/Users/christophermohammed/dev/tools/chromedriver', options=options)

    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 1000)

    values = get_inputs_from_sheet()
    for row in values:
        # search for user
        search_xpath = '//*[@id="side"]/div[1]/div/label/div'
        search_bar = wait.until(
            EC.presence_of_element_located((By.XPATH, search_xpath)))
        search_bar.send_keys(row[0] + Keys.ENTER)
        time.sleep(1)
        # select contact at the top of the list
        # inp_xpath = '//div[@class="input"][@dir="auto"][@data-tab="1"]'
        # input_box = wait.until(
        #     EC.presence_of_element_located((By.XPATH, inp_xpath)))
        # for i in range(100):
        #     input_box.send_keys(row[1] + Keys.ENTER)
        #     time.sleep(1)


if __name__ == '__main__':
    message_friends()
