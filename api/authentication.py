import requests
import json
import getpass
import os
from api.format import *

CUR_PATH = os.path.dirname(__file__)
CRED_PATH = '../credentials.json'


def check_response_status(res, printflag):
    if res.status_code != 200:
        raise Exception(f'{tformatting.FAIL}Error: Response Returned ' + str(res.status_code) + f'{tformatting.ENDC}')
    elif printflag:
        print(f'{tformatting.OKGREEN}  Request returned ' +
              str(res.status_code) + f'{tformatting.ENDC}')

# retrieve credentials from credentials.json
def get_credentials():
    credentials = {}

    try:
        with open(os.path.join(CUR_PATH, CRED_PATH), 'r') as json_file:
            credentials = json.load(json_file)
    except:
        print('credentials.json not found, please enter credentials')
        credentials['app_id'] = input('App id: ')
        credentials['secret'] = input('Secret: ')
        credentials['reddit_username'] = input('Reddit username: ')
        credentials['reddit_password'] = getpass.getpass('Reddit password: ')

    return credentials


class auth_obj:
    credentials = None
    token = None
    headers = None

    def __init__(self):
        self.headers = {'User-Agent': 'salestrackerbot/0.0.1'}
        self.credentials = get_credentials()
        self.token = self.set_token()

    def set_token(self):

        auth = requests.auth.HTTPBasicAuth(
            self.credentials['app_id'], self.credentials['secret'])

        data = {
            'grant_type': 'password',
            'username': self.credentials['reddit_username'],
            'password': self.credentials['reddit_password']
        }

        # post request to retrieve token
        post_res = requests.post('https://www.reddit.com/api/v1/access_token',
                                 auth=auth, data=data, headers=self.headers)
        check_response_status(post_res, True)

        token = post_res.json()['access_token']
        self.headers['Authorization'] = 'bearer {}'.format(token)

        # get request to verify get functionality with token works
        get_res = requests.get(
            'https://oauth.reddit.com/api/v1/me', headers=self.headers)
        check_response_status(get_res, True)

        token = post_res.json()['access_token']

        self.token = token

    def get_token(self):
        return self.token
