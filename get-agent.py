import requests
import urllib
import os
import json
import base64

class st_agent:

    def __init__(self):
        
        # External Parameters
        self.apikey = os.environ['APIKEY']
        self.apisecret = os.environ['APISECRET']
        self.orgname = os.environ['CUSTOMERID']
        
        # Place holders
        self.token = ''
        
        # Statiic default parameters
        self.output = '/tmp/smart-tools-agent.bin'

    def get_oAuthToken(self):
        
        # Get CompanyId
        url = make_url("https://smart.cloud.com/v0/companies?", { 'client_id' : self.apikey} )
        response = json.loads(requests.request("GET", url).text)
        data = (item for item in response if item["name"] == self.orgname)
        for item in data:
            companyid = str(item["companyId"])
            break
        
        # Get API client's role based on apikey
        url = make_url("https://smart.cloud.com/v0/roles?", { 'client_id' : self.apikey, 'company_id' : companyid})
        role = json.loads(requests.request("GET", url).text)[0]
        
        # Get OAuth Token
        url = make_url("https://smart.cloud.com/v0/oauth/token?", { 'grant_type' : 'client_credentials', 'scope' : role + "," + companyid})
        apikeysecret = self.apikey + ":" + self.apisecret
        apikeysecret = base64.b64encode(apikeysecret.encode())
        headers = {'Authorization': 'Basic ' + apikeysecret.decode('UTF-8') }
        self.token = json.loads(requests.request("GET", url, headers=headers).text)['access_token']

    def get_agent(self):
        url = make_url("https://smart.cloud.com/v0/download/info?", {'access_token' : self.token} )
        response = json.loads(requests.request("GET", url).text)
        data = (item for item in response['data'] if item['arch'] == 'deb32')
        for item in data:
            link = item["link"]
            break
        
        agent = requests.get(link, stream=True)
        with open(self.output, 'wb') as bin:
            for chunk in agent.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
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
