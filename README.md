# Python3-Oauth-Containers
Built on requests-oauth and shelve these OAuth classes were created to simplify calls the implementation of requests-oauth calls.

## OAuth2 - Google Example
```python
# Config Params
client_id = 'clientID'
client_secret = 'secret'
redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
token_url = "https://accounts.google.com/o/oauth2/token"
refresh_url = 'https://www.googleapis.com/oauth2/v3/token'
scope = ['https://www.googleapis.com/auth/urlshortener'] # Activate scopes at https://console.developers.google.com

# Get Request
googleOauth = OAuth2(client_id, client_secret, redirect_uri, authorization_base_url, token_url, refresh_url, scope)

def shorten(longUrl):
  # Get Session
	session = googleOauth.getSession()
	
	post_url = 'https://www.googleapis.com/urlshortener/v1/url'
	payload = {'longUrl': longUrl}
	headers = {'content-type': 'application/json'}
	
	response = session.post(post_url, data=json.dumps(payload), headers=headers)
```

## OAuth2 - LinkedIn Example
```python
# Config Params
client_id = 'clientID'
client_secret = 'secret'
redirect_uri = 'http://127.0.0.1'
authorization_base_url = "https://www.linkedin.com/uas/oauth2/authorization"
token_url = "https://www.linkedin.com/uas/oauth2/accessToken"
headers = {'content-type': 'application/json'}
refresh_url = None
scope = ['w_share']

# Get rquest
googleOauth = OAuth2(client_id, client_secret, redirect_uri, authorization_base_url, token_url, refresh_url, scope)

def getProfile():
	session = googleOauth.getSession()

	post_url = 'https://api.linkedin.com/v1/people/~?format=json'
	
	response = session.get(post_url, headers=headers)
```

## OAuth1 - Twitter Example
```python
# Config Params
client_key = 'clientKey'
client_secret = 'secret'
callback_uri = 'https://127.0.0.1/callback'

request_token_url = 'https://api.twitter.com/oauth/request_token'
authorization_url = 'https://api.twitter.com/oauth/authorize'
access_token_url = 'https://api.twitter.com/oauth/access_token'

# Get request
twitterOauth = OAuth1(client_key, client_secret, callback_uri, request_token_url, authorization_url, access_token_url)

def tweet(message):
  # Get Session
	session = twitterOauth.getSession()
	
	status_url = 'https://api.twitter.com/1.1/statuses/update.json'
	new_status = {'status': message}
	
	response = session.post(status_url, data=new_status)
```
