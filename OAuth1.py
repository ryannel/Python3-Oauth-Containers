import os 
from dataStore import dataStore
from requests_oauthlib import OAuth1Session

class OAuth1:
	def __init__(self, client_key, client_secret, callback_uri, request_token_url, authorization_url, access_token_url):
		self.client_key = client_key
		self.client_secret = client_secret
		self.callback_uri = callback_uri
		self.request_token_url = request_token_url
		self.authorization_url = authorization_url
		self.access_token_url = access_token_url
		
		self.token = self._getTokenFromDataStore()
		self.session = None
		
		if self.token == None:
			self.session = self.getSession()
		
	def _getTokenFromDataStore(self):
		try:
			return dataStore.get('tokens')[self.authorization_url]
		except KeyError:
			return None

	def _setTokenInDataStore(self, token):
		model = dataStore.get('tokens')
		model[self.authorization_url] = token
		dataStore.set('tokens', model)
		
	def getSession(self):
		if (self.token == None):
			self.createSession()
		elif (self.session == None):
			self._setSession()
		
		return self.session
	
	def createSession(self):
		session =  OAuth1Session(self.client_key, client_secret=self.client_secret, callback_uri=self.callback_uri)
		
		session.fetch_request_token(self.request_token_url)
		
		print('Please go here and authorize: ', session.authorization_url(self.authorization_url))
		
		redirect_response = input('Paste the full redirect URL here.')
		
		session.parse_authorization_response(redirect_response)
		
		access_token = session.fetch_access_token(self.access_token_url)
		
		self._setTokenInDataStore(access_token)
		self.token = access_token
		
		self.session = session
	
	def _setSession(self):
		self.session = OAuth1Session(self.client_key, client_secret=self.client_secret, resource_owner_key=self.token['oauth_token'], resource_owner_secret=self.token['oauth_token_secret'])

			
