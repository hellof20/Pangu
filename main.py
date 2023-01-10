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
# SCOPES = sql.get_scope()
SCOPES = ['https://www.googleapis.com/auth/userinfo.email']
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


@app.route('/apply', methods=['OPTIONS','GET','POST'])
def apply():
  DEPLOY_ID = request.form.get("deploy_id")
  solution_id = request.form.get("solution_id")
  need_scopes = sql.get_scope(solution_id).split(',')
  credentials = get_credentials()
  access_token = credentials.token
  refresh_token = credentials.refresh_token, 
  token_uri = credentials.token_uri,
  client_id = credentials.client_id,
  client_secret = credentials.client_secret,
  current_scopes = credentials.scopes
  if current_scopes == need_scopes:
    try:
      data = sql.get_deploy(DEPLOY_ID)[0]
      solution_id = data[0]
      url = data[1]
      deploy_path = data[2]
      deploy_type = data[3]
      parameters = "'" + data[4] + "'"
      command='bash apply.sh'
      result = run_as_docker(command,host,user,password,solution_id,DEPLOY_ID,url,deploy_path,deploy_type,parameters,client_id,client_secret,refresh_token,need_scopes,access_token)
      if result == 0:
        sql.update_deploy_status(DEPLOY_ID, 'deploying')
      else:
        sql.update_deploy_status(DEPLOY_ID, 'deploy_failed')
    except:
      return "something wrong, cant be deploy"
    else:
      return "deploying... please check deploy log"
  else:
    global SCOPES
    SCOPES = need_scopes
    return '0'


@app.route('/destroy', methods=['OPTIONS','GET','POST'])
def destroy():
  DEPLOY_ID = request.form.get("deploy_id")
  solution_id = request.form.get("solution_id")
  need_scopes = sql.get_scope(solution_id).split(',')  
  credentials = get_credentials()
  access_token = credentials.token
  refresh_token = credentials.refresh_token,
  token_uri = credentials.token_uri,
  client_id = credentials.client_id,
  client_secret = credentials.client_secret,
  current_scopes = credentials.scopes
  if current_scopes == need_scopes:  
    try:
      data = sql.get_deploy(DEPLOY_ID)[0]
      solution_id = data[0]
      url = data[1]
      deploy_path = data[2]
      deploy_type = data[3]
      parameters = "'" + data[4] + "'"
      command='bash destroy.sh'
      result = run_as_docker(command,host,user,password,solution_id,DEPLOY_ID,url,deploy_path,deploy_type,parameters,client_id,client_secret,refresh_token,need_scopes,access_token)
      if result == 0:
        sql.update_deploy_status(DEPLOY_ID, 'destroying')
      else:
        sql.update_deploy_status(DEPLOY_ID, 'destroy_failed')
    except:
      return "something wrong, cant be destroy"
    else:
      return "deleting... please check deploy log"
  else:
    global SCOPES
    SCOPES = need_scopes
    return '0'      

def run_as_cloudrun(command,host,user,password,solution_id,DEPLOY_ID,url,deploy_path,deploy_type,parameters,client_id,client_secret,refresh_token,scopes,access_token):
  create_job_command = ''' gcloud beta run jobs create %s \
    --image us.gcr.io/speedy-victory-336109/ads-job-dev:v0.2 \
    --tasks 1 \
    --set-env-vars host=%s \
    --set-env-vars user=%s \
    --set-env-vars password=%s \
    --set-env-vars solution_id=%s \
    --set-env-vars DEPLOY_ID=%s \
    --set-env-vars url=%s \
    --set-env-vars deploy_path=%s \
    --set-env-vars deploy_type=%s \
    --set-env-vars parameters=%s \
    --set-env-vars client_id=%s \
    --set-env-vars client_secret=%s \
    --set-env-vars refresh_token=%s \
    --set-env-vars scopes="%s" \
    --set-env-vars GOOGLE_APPLICATION_CREDENTIALS="/app/client_secret.json" \
    --set-env-vars CLOUDSDK_AUTH_ACCESS_TOKEN=%s \
    --max-retries 1 \
    --region us-central1 \
    --command %s
    ''' % (DEPLOY_ID,host,user,password,solution_id,DEPLOY_ID,url,deploy_path,deploy_type,parameters,client_id[0],client_secret[0],refresh_token[0],scopes,access_token,command)
  execute_job_command = 'gcloud beta run jobs execute %s' % DEPLOY_ID
  # create_job_result = os.system(create_job_command)
  # execute_job_result = os.system(execute_job_command)
  print(create_job_command)
  print(execute_job_command)
  if create_job_result == 0 and execute_job_result == 0:
    return 0
  else:
    return 1


def run_as_docker(command,host,user,password,solution_id,DEPLOY_ID,url,deploy_path,deploy_type,parameters,client_id,client_secret,refresh_token,scopes,access_token):
  command = 'docker rm -f task-'+ DEPLOY_ID +'  > /dev/null 2>&1;docker run --name task-'+ DEPLOY_ID +' -itd -e host=%s -e user=%s -e password=%s -e db=ads -e solution_id=%s -e DEPLOY_ID=%s -e url=%s -e deploy_path=%s -e deploy_type=%s -e parameters=%s -e client_id=%s -e client_secret=%s -e refresh_token=%s -e scopes="%s" -e GOOGLE_APPLICATION_CREDENTIALS="/app/client_secret.json" -e CLOUDSDK_AUTH_ACCESS_TOKEN=%s -e consul_ip=%s %s %s' % (host,user,password,solution_id,DEPLOY_ID,url,deploy_path,deploy_type,parameters,client_id[0],client_secret[0],refresh_token[0],scopes,access_token,consul_ip,image,command)
  print("docker command:",command)
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


@app.route('/describe_deploy', methods=['POST'])
def describe_deploy():
  DEPLOY_ID = request.form.get("deploy_id")
  SOLUTION_ID = request.form.get("solution_id")
  data = sql.describe_deploy(DEPLOY_ID, SOLUTION_ID)
  return data


@app.route('/create', methods=['OPTIONS','GET','POST'])
def create():
  credentials = get_credentials()
  access_token = credentials.token
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


@app.route('/list_parameter', methods=['POST'])
def list_parameter():
  credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])
  credentials = get_credentials()
  access_token = credentials.token
  email = get_user_email(access_token)
  request_data = request.get_json()
  solution_id = request_data["solution_id"]
  result = sql.list_parameter(solution_id, email, credentials)
  return result


@app.route('/authorize', methods=['GET','POST'])
def authorize():
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True, _scheme='https')
  authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true',prompt='consent')
  # authorization_url, state = flow.authorization_url(access_type='offline')
  flask.session['state'] = state
  print(authorization_url)
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
  #判断是否有refresh_token
  refresh_token = flask.session['credentials']['refresh_token']
  print('refresh_token is ',refresh_token)
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