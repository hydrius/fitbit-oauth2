#!/usr/bin/python3.5
# It All Starts With The Shebang!

import fitbit
import configparser
import time
import shutil
import os
import cherrypy
import threading
import timer
import webbrowser


from base64 import b64encode
from fitbit.api import FitbitOauth2Client
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError
from requests_oauthlib import OAuth2Session



class FitbitWrapper:

    def __init__(self, client_id=None, client_secret=None, config_dir=None):

        self.client_id = client_id
        self.client_secret = client_secret

        # If config_dir option is not entered, resort to current folder 
        self.config_dir = config_dir 
        if self.config_dir is None:
            self.config_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.config_path   = os.path.join(self.config_dir,'config.ini')

        # Import settings if the file exists, otherwise create user.
        if os.path.exists(self.config_path):
            self.importSettings() 
        else: 
            self.createUser()
 
        self.client = fitbit.Fitbit(self.client_id, self.client_secret, access_token=self.access_token, refresh_token=self.refresh_token)

    def importSettings(self):

        self.parser = configparser.ConfigParser()
        self.parser.read(self.config_path)
        
        try: 
           self.client_id     = self.parser.get("settings", 'client_id') 
           self.client_secret = self.parser.get("settings", 'client_secret')
           self.refresh_token = self.parser.get("settings", 'refresh_token')
           self.access_token  = self.parser.get("settings", 'access_token')
        except:
           print("Something went wrong")
           print("Creating new user")
           self.createUser()


    def createUser(self):
        self.redirect_uri = 'http://127.0.0.1:8080/'
        
        if self.client_id is None:
            print("Please enter your client_id")
            self.client_id = raw_input()
 
        if self.client_secret is None:      
            print("Please enter your client_secret")
            self.client_secret = raw_input()

        self.client = fitbit.Fitbit(self.client_id, self.client_secret)
        self.browser_authorise()
        self.refresh_token = self.client.client.token['refresh_token']
        self.access_token = self.client.client.token['access_token']
        self.saveTokens()

    def browser_authorise(self):
        url, _ = self.client.client.authorize_token_url(redirect_uri=self.redirect_uri)
        threading.Timer(1, webbrowser.open, args=(url,)).start()
        cherrypy.quickstart(self)

    @cherrypy.expose
    def index(self,state,code=None, error=None):

        if code:
           try:
              self.client.client.fetch_access_token(code, redirect_uri = self.redirect_uri)
           except MissingTokenError:
              print("missing token again")

        self._shutdown_cherrypy()
        
        return error

    def _shutdown_cherrypy(self):
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()


    def saveTokens(self):

        if os.path.exists(self.config_path):
            os.remove(self.config_path)

        with open(self.config_path, "w") as file:

            self.parser = configparser.ConfigParser()

            self.parser.add_section("settings")
            self.parser.set("settings", 'refresh_token', self.refresh_token)
            self.parser.set("settings", 'access_token', self.access_token)
            self.parser.set("settings", 'client_id', self.client_id)        
            self.parser.set("settings", 'client_secret', self.client_secret)

            self.parser.write(file)


    def refresh(self):
         
        self.client.client.refresh_token()
        self.saveTokens()
        

        self.refresh_token = self.client.client.token['refresh_token']
        self.access_token = self.client.client.token['access_token']
        self.saveTokens()

    def run(self):
        while True:
            
            self.refresh() 

            print(self.client.sleep())
            time.sleep(30)


if __name__ == '__main__':
    fitbit = FitbitWrapper()

