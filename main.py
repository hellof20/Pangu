# -*- coding: utf-8 -*-

import os,subprocess
import flask
import requests
from flask import request,render_template,send_file,jsonify
import json
import sql
from flask_cors import CORS

import google.oauth2.credentials
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from google.ads.googleads.client import GoogleAdsClient

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['openid','https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/compute','https://www.googleapis.com/auth/cloud-platform','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/appengine.admin','https://www.googleapis.com/auth/datastore','https://www.googleapis.com/auth/adsdatahub']
API_SERVICE_NAME = 'compute'
API_VERSION = 'v1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = flask.Flask(__name__)
CORS(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'xxxxxxx'
REDIRECT_URI ='urn:ietf:wg:oauth:2.0:oob'

host = os.getenv('host')
user = os.getenv('user')
password = os.getenv('password')
image = os.environ.get('image')
consul_ip = os.environ.get('consul_ip')


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/disclaimer')
def disclaimer():
  return render_template('disclaimer.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/oauth')
def oauth():
  return render_template('oauth.html')

@app.route('/list_deploy_email', methods=['OPTIONS','GET','POST'])
def list_deploy_email():
  credentials = get_credentials()
  access_token = credentials.token
  email = get_user_email(access_token)
  result = sql.list_deploy_email(email)
  return result

@app.route('/list_parameter', methods=['POST'])
def list_parameter():
  credentials = get_credentials()
  access_token = credentials.token
  email = get_user_email(access_token)
  request_data = request.get_json()
  solution_id = request_data["solution_id"]
  result = sql.list_parameter(solution_id, email, credentials)
  return result


@app.route('/deploy', methods=['OPTIONS','GET','POST'])
def deploy():
  credentials = get_credentials()
  access_token = credentials.token
  refresh_token = credentials.refresh_token 
  token_uri = credentials.token_uri
  client_id = credentials.client_id
  client_secret = credentials.client_secret  
  email = get_user_email(access_token)
  parameters = request.get_json()
  solution_id = parameters["solution_id"]
  project_id = parameters["project_id"]
  version = parameters["version"]
  deploy_type = parameters["deploy_type"]
  del parameters["solution_id"]
  for k,v in parameters.items():
    if k!= 'version' and v == '':
      return 'parameters cant be empty'
  deploy_id = sql.insert_deploy(solution_id,project_id,email,version,deploy_type)
  try:
    data = sql.get_solution(solution_id,deploy_type)[0]
    url = data[0]
    deploy_path = data[1]
    command='bash apply.sh'
    result = run_as_docker(command,host,user,password,solution_id,deploy_id,url,deploy_path,deploy_type,"'"+json.dumps(parameters)+"'",client_id,client_secret,refresh_token,SCOPES,access_token)
    if result == 0:
      sql.update_deploy_status(deploy_id, 'deploying')
    else:
      sql.update_deploy_status(deploy_id, 'deploy_failed')
  except:
    return "something wrong, cant be deploy"
  else:
    return "deploying... please check deploy log"


def run_as_docker(command,host,user,password,solution_id,DEPLOY_ID,url,deploy_path,deploy_type,parameters,client_id,client_secret,refresh_token,scopes,access_token):
  command = 'docker rm -f task-'+ DEPLOY_ID +'  > /dev/null 2>&1;docker run --name task-'+ DEPLOY_ID +' -itd -e host=%s -e user=%s -e password=%s -e db=ads -e solution_id=%s -e DEPLOY_ID=%s -e url=%s -e deploy_path=%s -e deploy_type=%s -e parameters=%s -e client_id=%s -e client_secret=%s -e refresh_token=%s -e scopes="%s" -e GOOGLE_APPLICATION_CREDENTIALS="/app/client_secret.json" -e CLOUDSDK_AUTH_ACCESS_TOKEN=%s -e consul_ip=%s %s %s' % (host,user,password,solution_id,DEPLOY_ID,url,deploy_path,deploy_type,parameters,client_id,client_secret,refresh_token,scopes,access_token,consul_ip,image,command)
  result = os.system(command)
  return result


@app.route('/deletetask', methods=['POST'])
def deletetask():
  DEPLOY_ID = request.form.get("deploy_id")
  command = 'docker rm -f task-'+ DEPLOY_ID +' > /dev/null 2>&1;'
  os.system(command)
  try:
    result = sql.delete_task(DEPLOY_ID)
  except:
    return 'delete task failed!'
  else:
    return result


@app.route('/deploylog', methods=['OPTIONS','GET','POST'])
def deploylog():
  DEPLOY_ID = request.form.get("deploy_id")
  command = 'docker logs task-'+ DEPLOY_ID +''
  log = os.system(command + "> /tmp/" + DEPLOY_ID +".log 2>&1")
  try:
    if os.path.exists("/tmp/%s.log" % (DEPLOY_ID)):
      return send_file("/tmp/%s.log" % (DEPLOY_ID))
    else:
      return 'deploy log is not existing'
  except:
    return 'get deploy log failed'
  

@app.route('/get_authorize_url/')
def get_authorize_url():
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')
    solution_id = request.args.get('solution_id')
    scopes= sql.get_scope(solution_id).split(',')
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
    scopes= sql.get_scope(solution_id).split(',')
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


@app.route('/list_solution', methods=['GET'])
def list_solution():
  result = sql.list_solution()
  return result


@app.route('/list_solution_detail', methods=['GET'])
def list_solution_detail():
  result = sql.list_solution_detail()
  return result


@app.route('/authorize', methods=['GET','POST'])
def authorize():
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True, _scheme='https')
  authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='false',prompt='consent')
  flask.session['state'] = state
  return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
  # state = flask.session['state']
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True, _scheme='https')
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)
  credentials = flow.credentials
  flask.session['credentials'] = credentials_to_dict(credentials)
  refresh_token = flask.session['credentials']['refresh_token']
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
  flask.session['credentials'] = credentials_to_dict(credentials)
  return credentials


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