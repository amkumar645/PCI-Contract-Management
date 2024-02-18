import flask
import os
from urllib.parse import urlencode
import requests
import database
import models
from datetime import datetime
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
# General Functions
#----------------------------------------------------------------------
def check_authentication():
  google_token = flask.session.get('google_token')
  return google_token is not None

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

# Home page
@app.route('/home', methods=['GET'])
def home():
  if not check_authentication():
    return flask.redirect(flask.url_for('error_page'))
  email = flask.session.get("email")
  html = flask.render_template('templates/home.html', 
            employee=database.get_employee(email)
          )
  response = flask.make_response(html)
  return response

# Error page
@app.route('/unauthorized', methods=['GET'])
def error_page():
  html = flask.render_template('templates/unauthorized.html')
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
  return flask.redirect(flask.url_for('index'))

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

  email = user_info['email']
  if "programcontrolsinc" not in email and "amkumar@princeton.edu" not in email:
    flask.session.pop('google_token', None)
    return flask.redirect(flask.url_for('error_page'))

  # Store token in session
  flask.session['google_token'] = (access_token, '')

  # Get employee
  employee = database.get_employee(email)
  if employee is None:
    employee = models.Employees(
      email = email,
      name = email,
      position = "",
      authorization = "Employee",
      projects = []
    )
    database.add_employee(employee)
  
  flask.session['email'] = email

  return flask.redirect(flask.url_for('home'))

#----------------------------------------------------------------------
# Contracts Routes
#----------------------------------------------------------------------
# Contracts Main Page
@app.route('/contracts', methods=['GET'])
def contracts_main():
  if not check_authentication():
    return flask.redirect(flask.url_for('error_page'))
  email = flask.session.get("email")
  contracts = database.get_all_contracts()
  html = flask.render_template('templates/contracts.html', 
          employee=database.get_employee(email),
          contracts=contracts
        )
  response = flask.make_response(html)
  return response

# Contracts Individual Page
@app.route('/contracts/<number>', methods=['GET'])
def contract(number):
  if not check_authentication():
    return flask.redirect(flask.url_for('error_page'))
  email = flask.session.get("email")
  contract = database.get_contract_by_number(number)
  auths = database.get_all_authorizations_by_contract_number(number)
  invoices = database.get_all_invoices_by_contract_number(number)
  html = flask.render_template('templates/contractpage.html', 
          employee=database.get_employee(email),
          contract=contract,
          auths=auths,
          invoices=invoices
        )
  response = flask.make_response(html)
  return response

#----------------------------------------------------------------------
# Authorizations Routes
#----------------------------------------------------------------------
@app.route('/authorizations', methods=['GET'])
def auths_main():
  if not check_authentication():
    return flask.redirect(flask.url_for('error_page'))
  email = flask.session.get("email")
  auths = database.get_all_authorizations()
  html = flask.render_template('templates/auths.html', 
          employee=database.get_employee(email),
          auths=auths
        )
  response = flask.make_response(html)
  return response

# Auth Individual Page
@app.route('/authorizations/<number>', methods=['GET'])
def authorization(number):
  if not check_authentication():
    return flask.redirect(flask.url_for('error_page'))
  email = flask.session.get("email")
  auth = database.get_authorization_by_number(number)
  invoices = database.get_all_invoices_by_contract_auth_number(number)
  html = flask.render_template('templates/authpage.html', 
          employee=database.get_employee(email),
          auth=auth,
          invoices=invoices
        )
  response = flask.make_response(html)
  return response

#----------------------------------------------------------------------
# Invoices Routes
#----------------------------------------------------------------------
@app.route('/invoices', methods=['GET'])
def invoices_main():
  if not check_authentication():
    return flask.redirect(flask.url_for('error_page'))
  email = flask.session.get("email")
  invoices = database.get_all_invoices()
  html = flask.render_template('templates/invoices.html', 
          employee=database.get_employee(email),
          invoices=invoices
        )
  response = flask.make_response(html)
  return response

# Invoice Individual Page
@app.route('/invoices/<number>', methods=['GET'])
def invoice(number):
  if not check_authentication():
    return flask.redirect(flask.url_for('error_page'))
  email = flask.session.get("email")
  invoice = database.get_invoice_by_number(number)
  html = flask.render_template('templates/invoicepage.html', 
          employee=database.get_employee(email),
          invoice=invoice,
        )
  response = flask.make_response(html)
  return response

#----------------------------------------------------------------------
# Profile Routes
#----------------------------------------------------------------------
@app.route('/profile', methods=['GET'])
def profile_main():
  if not check_authentication():
    return flask.redirect(flask.url_for('error_page'))
  email = flask.session.get("email")
  employee = database.get_employee(email)
  html = flask.render_template('templates/profile.html', 
          employee=employee,
          contracts =database.get_employee_contracts(employee.projects)
        )
  response = flask.make_response(html)
  return response

#----------------------------------------------------------------------
# Timesheet Routes
#----------------------------------------------------------------------
@app.route('/timesheet', methods=['GET'])
def timesheet():
  if not check_authentication():
    return flask.redirect(flask.url_for('error_page'))
  email = flask.session.get("email")
  employee = database.get_employee(email)
  today = datetime.now()
  year = today.strftime("%Y")
  week_number = today.strftime("%V")
  week = f"{year}-W{week_number}"
  timesheet = database.get_timesheet_by_date(employee.email + "-" + week)
  html = flask.render_template('templates/timesheet.html', 
          employee=employee,
          timesheet=timesheet
        )
  response = flask.make_response(html)
  return response