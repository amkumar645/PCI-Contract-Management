import flask
import os
from urllib.parse import urlencode
import requests
#----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')
app.secret_key = os.getenv('SECRET_KEY')

# Google OAuth configuration
google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_client_secret = os.getenv('GOOGLE_SECRET')
google_authorize_url = 'https://accounts.google.com/o/oauth2/auth'
google_token_url = 'https://accounts.google.com/o/oauth2/token'
google_userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'

#----------------------------------------------------------------------
# General Routes
#----------------------------------------------------------------------
# Landing page
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html = flask.render_template('templates/landing.html')
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------
# Login Routes
#----------------------------------------------------------------------
@app.route('/login')
def login():
  params = {
    'client_id': google_client_id,
    'redirect_uri': flask.url_for('authorized', _external=True),
    'scope': 'email',
    'response_type': 'code',
  }
  auth_url = f"{google_authorize_url}?{urlencode(params)}"
  return flask.redirect(auth_url)

@app.route('/logout')
def logout():
  flask.session.pop('google_token', None)
  return 'Logged out successfully'

@app.route('/login/google/callback')
def authorized():
  auth_code = flask.request.args.get('code')
  token_data = {
    'code': auth_code,
    'client_id': google_client_id,
    'client_secret': google_client_secret,
    'redirect_uri': flask.url_for('authorized', _external=True),
    'grant_type': 'authorization_code',
  }

  # Request access token
  token_response = requests.post(google_token_url, data=token_data)
  access_token = token_response.json().get('access_token')

  # Request user information
  userinfo_response = requests.get(google_userinfo_url, headers={'Authorization': f'Bearer {access_token}'})
  user_info = userinfo_response.json()

  # Store token in session
  flask.session['google_token'] = (access_token, '')

  # Here you can use user_info to get user details like email, name, etc.
  print(user_info)

  return 'Logged in as: ' + user_info['email']
