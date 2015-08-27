import os 
import requests
import time
from dataStore import dataStore
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class OAuth2:
	def __init__(self, client_id, client_secret, redirect_uri, authorization_base_url, token_url, refresh_url, scope):
		self.client_id = client_id
		self.client_secret = client_secret
		self.redirect_uri = redirect_uri
		self.authorization_base_url = authorization_base_url
		self.token_url = token_url
		self.refresh_url = refresh_url
		self.scope = scope
		
		self.token = self._getTokenFromDataStore()
		self.session = None
		
		if self.token == None:
			self.session = self.getSession()
		
	def _getTokenFromDataStore(self):
		try:
			return dataStore.get('tokens')[self.authorization_base_url]
		except KeyError:
			return None

	def _setTokenInDataStore(self, token):
		model = dataStore.get('tokens')
		model[self.authorization_base_url] = token
		dataStore.set('tokens', model)
		
	def getSession(self):
		if (self.token == None):
			return self.createSession()
		elif (self.session == None):
			self._setSession()
		
		if (self._validateToken() == False):
			self.refreshToken()
			
		return self.session
	
	def createSession(self):
		session = OAuth2Session(self.client_id, scope=self.scope, redirect_uri=self.redirect_uri)
		
		if(self.authorization_base_url == 'https://www.linkedin.com/uas/oauth2/authorization'):
			session = linkedin_compliance_fix(session)
			
		authorization_url, state = session.authorization_url(self.authorization_base_url, access_type="offline", approval_prompt="force")
		
		print('Please go here and authorize,', authorization_url)
		
		redirect_response = input('Paste the full authorization token here:')
		
		session.fetch_token(self.token_url, client_secret=self.client_secret, code=redirect_response, verify=False)
		
		self._setTokenInDataStore(session.token)
		self.token = session.token
		
		return session
	
	def _setSession(self):
		self.session = OAuth2Session(self.client_id, scope=self.scope, token=self.token)
		
	def refreshToken(self):
		if self.token == None:
			raise ValueError('No token exists')
			
		if self.refresh_url == None:
			raise ValueError('No refresh Url')
		
		extra = {
		    'client_id': self.client_id,
		    'client_secret': self.client_secret,
		}
		
		self.token = self.session.refresh_token(self.refresh_url, refresh_token=self.token['refresh_token'], verify=False, **extra)
		self._setTokenInDataStore(self.token)
		
	def _validateToken(self):
		if self.token == None:
			raise ValueError('No token exists')
		
		if self.token['expires_at'] <= time.time():
			return False
		else:
			return True
