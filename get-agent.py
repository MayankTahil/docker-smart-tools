import requests
import urllib
import os
import json
import base64


class st_agent:

    def __init__(self):

        # External Parameters
        with open('secrets.json') as json_data:
            secrets = json.load(json_data)
            self.apikey = secrets['apikey']
            self.apisecret = secrets['apisecret']
            self.orgname = secrets['customerid']

        # Place holders
        self.token = ''
        self.companyid = ''
        self.role = ''

        # Static default parameters
        self.output = os.path.dirname(
            os.path.realpath(__file__)) + '/install_agent.bin'
        self.debug = False

    def get_oAuthToken(self):

        # Get CompanyId
        url = make_url("https://smart.cloud.com/v0/companies?",
                       {'client_id': self.apikey})
        response = json.loads(requests.request("GET", url).text)
        if self.debug:
            debug(response)
        data = (item for item in response if item["name"] == self.orgname)
        for item in data:
            self.companyid = str(item["companyId"])
            break

        # Get API client's role based on apikey
        url = make_url("https://smart.cloud.com/v0/roles?",
                       {'client_id': self.apikey,
                        'company_id': self.companyid})
        self.role = json.loads(requests.request("GET", url).text)[0]
        if self.debug:
            debug(self.role)

        # Get OAuth Token
        url = make_url("https://smart.cloud.com/v0/oauth/token?",
                       {'grant_type': 'client_credentials',
                        'scope': self.role + "," + self.companyid})
        apikeysecret = self.apikey + ":" + self.apisecret
        apikeysecret = base64.b64encode(apikeysecret.encode())
        headers = {'Authorization': 'Basic ' + apikeysecret.decode('UTF-8')}
        self.token = json.loads(requests.request(
            "GET", url, headers=headers).text)['access_token']
        if self.debug:
            debug(self.token)

    def get_agent(self):
        url = make_url("https://smart.cloud.com/v0/download/info?",
                       {'access_token': self.token})
        response = json.loads(requests.request("GET", url).text)
        if self.debug:
            debug(response)
        data = (item for item in response['data'] if item['arch'] == 'deb64')
        for item in data:
            link = item["link"]
            break

        agent = requests.get(link, stream=True)
        with open(self.output, 'wb') as bin:
            for chunk in agent.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    bin.write(chunk)


def make_url(base, append):
    append = urllib.parse.urlencode(append)
    url = base + append
    return url


def debug(response):
    print(json.dumps(response, indent=4, sort_keys=True))

if __name__ == '__main__':
    """ This is our main thread of execution, it starts all the work!"""

    agent = st_agent()
    agent.get_oAuthToken()
    agent.get_agent()
