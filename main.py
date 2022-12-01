# -*- coding: utf-8 -*-

import os,subprocess
import flask
import requests
from flask import request,render_template,send_file,jsonify
import json
import sql

import google.oauth2.credentials
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from google.ads.googleads.client import GoogleAdsClient

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = sql.get_scope()
API_SERVICE_NAME = 'compute'
API_VERSION = 'v1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = flask.Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'xxxxxxx'
REDIRECT_URI ='urn:ietf:wg:oauth:2.0:oob'


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/oauth')
def oauth():
  return render_template('oauth.html')

@app.route('/list_deploy_email', methods=['OPTIONS','GET','POST'])
def list_deploy_email():
  access_token = get_credentials()
  email = get_user_email(access_token)
  result = sql.list_deploy_email(email)
  return result
  

@app.route('/apply', methods=['OPTIONS','GET','POST'])
def apply():
  access_token = get_credentials()
  DEPLOY_ID = request.form.get("deploy_id")
  try:
    data = json.loads(sql.get_deploy(DEPLOY_ID))
    solution_id = data[0]
    url = data[1]
    tf_path = data[2]
    deploy_type = data[3]
    bash_path = data[4]
    version = data[5]
    # print("solution_id = ",solution_id)
    # print("url = ",url)
    # print("DEPLOY_ID = ",DEPLOY_ID)
    # print("tf_path = ",tf_path)
    # print("deploy_type = ",deploy_type)
    # print("bash_path = ",bash_path)
    # print("access_token = ",access_token)
    subprocess.Popen('export solution_id=%s DEPLOY_ID=%s url=%s tf_path=%s deploy_type=%s bash_path=%s access_token=%s version=%s && bash apply.sh' % (solution_id,DEPLOY_ID,url,tf_path,deploy_type,bash_path,access_token,version), shell=True )
    sql.update_deploy_status(DEPLOY_ID, 'deploying')
  except:
    return "something wrong, cant be deploy"
  else:
    return "deploying... please check deploy log"


@app.route('/destroy', methods=['OPTIONS','GET','POST'])
def destroy():   
  access_token = get_credentials()
  DEPLOY_ID = request.form.get("deploy_id")
  data = json.loads(sql.get_deploy(DEPLOY_ID))
  solution_id = data[0]
  tf_path = data[2]
  deploy_type = data[3]
  bash_path = data[4]  
  subprocess.Popen('export DEPLOY_ID=%s access_token=%s solution_id=%s tf_path=%s deploy_type=%s bash_path=%s && bash destroy.sh' % (DEPLOY_ID,access_token,solution_id,tf_path,deploy_type,bash_path), shell=True )
  sql.update_deploy_status(DEPLOY_ID, 'destroying')
  return "deleting... please check deploy log"


@app.route('/upgrade', methods=['OPTIONS','GET','POST'])
def upgrade():
  access_token = get_credentials()
  DEPLOY_ID = request.form.get("deploy_id")
  data = json.loads(sql.get_deploy(DEPLOY_ID))
  solution_id = data[0]
  url = data[1]
  tf_path = data[2]
  print("access_token = ",access_token)
  subprocess.Popen('export DEPLOY_ID=%s url=%s access_token=%s solution_id=%s tf_path=%s && bash upgrade.sh' % (DEPLOY_ID, url, access_token, solution_id,tf_path), shell=True )
  sql.update_deploy_status(DEPLOY_ID, 'upgrading')
  return 'updating... please check deploy log'


@app.route('/deploylog', methods=['OPTIONS','GET','POST'])
def deploylog():
  deploy_path='/data/pangu'
  DEPLOY_ID = request.form.get("deploy_id")
  data = json.loads(sql.get_deploy(DEPLOY_ID))
  solution_id = data[0]
  try:
    if os.path.exists('%s/%s/deploy.log' % (deploy_path,DEPLOY_ID)):
      return send_file('%s/%s/deploy.log' % (deploy_path,DEPLOY_ID))
    else:
      return 'deploy log is not existing'
  except:
    return 'get deploy log failed'


@app.route('/describe_deploy', methods=['POST'])
def describe_deploy():
  DEPLOY_ID = request.form.get("deploy_id")
  SOLUTION_ID = request.form.get("solution_id")
  data = sql.describe_deploy(DEPLOY_ID, SOLUTION_ID)
  return data


@app.route('/create', methods=['OPTIONS','GET','POST'])
def create():
    access_token = get_credentials()
    email = get_user_email(access_token)
    parameters = request.get_json()
    SOLUTION = parameters["solution_id"]
    PROJECT_ID = parameters["project_id"]
    del parameters["solution_id"]
    for k,v in parameters.items():
      if k!= 'version' and v == '':
        return 'parameters cant be empty'
    result = sql.insert_deploy(SOLUTION,PROJECT_ID,email,parameters)
    return result


@app.route('/update_parameters', methods=['OPTIONS','GET','POST'])
def update_parameters():
    parameters = request.get_json()
    deploy_id = parameters['deploy_id']
    del parameters['deploy_id']
    for k,v in parameters.items():
      if k!= 'version' and v == '':
        return 'parameters cant be empty'
    sql_result = sql.update_parameters(deploy_id,parameters)
    if sql_result == 'success':
        return 'update successed'
    else:
        return 'update failed'
    


@app.route('/get_authorize_url/')
def get_authorize_url():
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')
    solution_id = request.args.get('solution_id')
    scopes= sql.get_solution_scope(solution_id)[0].split(',')
    print(scopes)
    flow = InstalledAppFlow.from_client_config(
          client_config={
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://oauth2.googleapis.com/token"
            }
      },scopes=scopes, redirect_uri=REDIRECT_URI
    )
    url, state = flow.authorization_url()
    return jsonify({'ok': 'true', 'name': 'get_authorize_url', 'data': {'url': url}})


@app.route('/fetch_token/')
def fetch_token():
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')  
    code = request.args.get('code')
    solution_id = request.args.get('solution_id')
    scopes= sql.get_solution_scope(solution_id)[0].split(',')
    flow = InstalledAppFlow.from_client_config(
          client_config={
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://oauth2.googleapis.com/token"
            }
      },scopes=scopes, redirect_uri=REDIRECT_URI
    )
    try:
        credentials = flow.fetch_token(code=code)
        return jsonify({'ok': 'true', 'name': 'fetch_token', 'data': {'credentials': credentials}})
    except Exception as e:
        print(e)
        return jsonify({'ok': 'false', 'name': 'fetch_token'})


@app.route('/list_campaigns/')
def list_campaigns():
    login_customer_id = request.args.get('login_customer_id')
    login_customer_id = str(login_customer_id).replace('-', '').strip()
    customer_id = request.args.get('customer_id')
    customer_id = str(customer_id).replace('-', '').strip()
    refresh_token = request.args.get('refresh_token')
    developer_token = request.args.get('developer_token')
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')  
    
    ads_config_dict = {
        'developer_token': developer_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'login_customer_id': login_customer_id,
        'use_proto_plus': True,
    }

    # print('----------------')
    # print(ads_config_dict)
    # print('----------------')

    try:
        client = GoogleAdsClient.load_from_dict(ads_config_dict)
        client.login_customer_id = login_customer_id
        ga_service = client.get_service("GoogleAdsService")
        query = '''
        SELECT
        campaign.id,
        campaign.name,
        campaign.status
        FROM campaign
        ORDER BY campaign.id
        '''
        search_request = client.get_type("SearchGoogleAdsStreamRequest")
        search_request.customer_id = customer_id
        search_request.query = query
        stream = ga_service.search_stream(search_request)
        campaigns = []
        for batch in stream:
            for row in batch.results:
                campaigns.append({
                    'resource_name': str(row.campaign.resource_name),
                    'status': str(row.campaign.status),
                    'name': str(row.campaign.name),
                    'id': str(row.campaign.id)
                })
        return jsonify({'ok': 'true', 'name': 'list_campaigns', 'data': {'campaigns': campaigns}})
    except Exception as e:
        print(e)
        return jsonify({'ok': 'false', 'name': 'list_campaigns'})



@app.route('/list_solution', methods=['GET','POST'])
def list_solution():
  result = sql.list_solution()
  return result

# @app.route('/list_solution_version', methods=['GET','POST'])
# def list_solution_version():
#   request_data = request.get_json()
#   print(request_data)
#   solution_id = request_data["solution_id"]
#   result = sql.list_solution_version(solution_id)
#   return result

@app.route('/list_parameter', methods=['POST'])
def list_parameter():
  credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])
  access_token = get_credentials()
  email = get_user_email(access_token)
  request_data = request.get_json()
  solution_id = request_data["solution_id"]
  result = sql.list_parameter(solution_id, email, credentials)
  return result


@app.route('/authorize')
def authorize():
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True, _scheme='https')
  authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
  # authorization_url, state = flow.authorization_url(access_type='offline')
  # print(authorization_url)
  flask.session['state'] = state
  return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
  state = flask.session['state']
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True, _scheme='https')
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)
  credentials = flow.credentials
  # access_token = credentials.token
  flask.session['credentials'] = credentials_to_dict(credentials)
  return flask.redirect('/')


@app.route('/revoke')
def revoke():
  if 'credentials' not in flask.session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')
  credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])
  revoke = requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})
  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.')
  else:
    return('An error occurred.')


@app.route('/clear')
def clear_credentials():
  if 'credentials' in flask.session:
    del flask.session['credentials']
  return ('Credentials have been cleared.')


def get_user_email(access_token):
  resp = requests.get('https://www.googleapis.com/oauth2/v3/userinfo?alt=json', headers={'Authorization': f'Bearer {access_token}'})
  result = resp.json()
  email = result['email']
  return email


def get_credentials():
  credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])
  access_token = credentials.token
  flask.session['credentials'] = credentials_to_dict(credentials)
  return access_token


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}          


if __name__ == '__main__':
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  app.run('0.0.0.0', 8080, debug=True)