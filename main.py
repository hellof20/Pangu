# -*- coding: utf-8 -*-

import os,subprocess
import flask
import requests
from flask import request,render_template,send_file
import json
import sql

import google.oauth2.credentials
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = sql.get_scope()
API_SERVICE_NAME = 'compute'
API_VERSION = 'v1'

app = flask.Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'xxxxxxx'

@app.route('/login')
def index():
  return render_template('login.html')


@app.route('/')
def ads():
  return render_template('index.html')


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
  data = json.loads(sql.get_deploy(DEPLOY_ID))
  solution_id = data[0]
  url = data[1]
  tf_path = data[2]
  print("solution_id = ",solution_id)
  print("url = ",url)
  print("DEPLOY_ID = ",DEPLOY_ID)
  print("tf_path = ",tf_path)
  subprocess.Popen('export solution_id=%s DEPLOY_ID=%s url=%s tf_path=%s access_token=%s && bash apply.sh' % (solution_id,DEPLOY_ID,url,tf_path,access_token), shell=True )
  sql.update_deploy_status(DEPLOY_ID, 'deploying..')
  return "部署中。。。 请等待"


@app.route('/destroy', methods=['OPTIONS','GET','POST'])
def destroy():   
  access_token = get_credentials()
  DEPLOY_ID = request.form.get("deploy_id")
  data = json.loads(sql.get_deploy(DEPLOY_ID))
  solution_id = data[0]
  tf_path = data[2]
  subprocess.Popen('export DEPLOY_ID=%s access_token=%s solution_id=%s tf_path=%s && bash destroy.sh' % (DEPLOY_ID,access_token,solution_id,tf_path), shell=True )
  sql.update_deploy_status(DEPLOY_ID, 'deleting..')
  return "删除中。。。 请等待"


@app.route('/upgrade', methods=['OPTIONS','GET','POST'])
def upgrade():
  access_token = get_credentials()
  DEPLOY_ID = request.form.get("deploy_id")
  data = json.loads(sql.get_deploy(DEPLOY_ID))
  solution_id = data[0]
  url = data[1]
  tf_path = data[2]
  subprocess.Popen('export DEPLOY_ID=%s url=%s access_token=%s solution_id=%s tf_path=%s && bash upgrade.sh' % (DEPLOY_ID, url, access_token, solution_id,tf_path), shell=True )
  sql.update_deploy_status(DEPLOY_ID, 'upgrading..')
  return '更新中。。。请等待'


@app.route('/deploylog', methods=['OPTIONS','GET','POST'])
def deploylog():
  DEPLOY_ID = request.form.get("deploy_id")
  data = json.loads(sql.get_deploy(DEPLOY_ID))
  solution_id = data[0]
  try:
    if os.path.exists('/tmp/%s/%s/deploy.log' % (DEPLOY_ID,solution_id)):
      return send_file('/tmp/%s/%s/deploy.log' % (DEPLOY_ID,solution_id))
    else:
      return '日志文件不存在'
  except:
    return '获取日志出错'


@app.route('/describe_deploy', methods=['POST'])
def describe_deploy():
  DEPLOY_ID = request.form.get("deploy_id")
  data = sql.describe_deploy(DEPLOY_ID)
  return data


@app.route('/create', methods=['OPTIONS','GET','POST'])
def create():
    access_token = get_credentials()
    email = get_user_email(access_token)
    parameters = request.get_json()
    for k,v in parameters.items():
      if v == '':
        return '参数不能为空'
    SOLUTION = parameters["solution_id"]
    PROJECT_ID = parameters["project_id"]
    sql.insert_deploy(SOLUTION,PROJECT_ID,email,parameters)
    return '创建部署任务成功'


@app.route('/get_authorize_url', methods=['POST'])
def get_authorize_url():
  access_token = get_credentials()
  email = get_user_email(access_token)
  parameters = request.get_json()
  for k,v in parameters.items():
    if v == '':
      return '参数不能为空'
  client_id = parameters["client_id"]
  client_secret = parameters["client_secret"]
  # print('client_id = ', client_id)
  # print('client_secret = ', client_secret)
  # flow = InstalledAppFlow.from_client_secrets_file('client_secret_886706209177-maog8ukjd7p096u3obvt45hlicvvdjkk.apps.googleusercontent.com.json', ['https://www.googleapis.com/auth/gmail.readonly'], redirect_uri='urn:ietf:wg:oauth:2.0:oob')

  # todo
  # solution scope从数据库获取

  flow = InstalledAppFlow.from_client_config(
            client_config={
              "installed": {
                  "client_id": client_id,
                  "client_secret": client_secret,
                  "redirect_uris": ["http://localhost", "urn:ietf:wg:oauth:2.0:oob"],
                  "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                  "token_uri":"https://oauth2.googleapis.com/token"
              }
        },scopes=['https://www.googleapis.com/auth/gmail.readonly'], redirect_uri='urn:ietf:wg:oauth:2.0:oob'
  )
  url, state = flow.authorization_url()
  return url


@app.route('/fetch_token', methods=['POST'])
def fetch_token():
  access_token = get_credentials()
  email = get_user_email(access_token)
  parameters = request.get_json()
  code = parameters["code"]
  solution_id = parameters["solution_id"]
  client_id = parameters["client_id"]
  client_secret = parameters["client_secret"]
  flow = InstalledAppFlow.from_client_config(
        client_config={
          "installed": {
              "client_id": client_id,
              "client_secret": client_secret,
              "redirect_uris": ["http://localhost", "urn:ietf:wg:oauth:2.0:oob"],
              "auth_uri":"https://accounts.google.com/o/oauth2/auth",
              "token_uri":"https://oauth2.googleapis.com/token"
          }
    },scopes=['https://www.googleapis.com/auth/gmail.readonly'], redirect_uri='urn:ietf:wg:oauth:2.0:oob'
  )
  try:
    credentials = flow.fetch_token(code=code)
    refresh_token = credentials['refresh_token']
    print('refresh_token = ',refresh_token)
    sql.insert_client_id_secret_token(email, solution_id, client_id, client_secret, refresh_token)
    return json.dumps({'ok': 'true'})
  except Exception as e:
    print(e)
    return json.dumps({'ok': 'false'})

@app.route('/list_solution', methods=['POST'])
def list_solution():
  result = sql.list_solution()
  return result


@app.route('/list_parameter', methods=['POST'])
def list_parameter():
  access_token = get_credentials()
  email = get_user_email(access_token)
  solution_id = request.form.get("solution_id")
  result = sql.list_parameter(solution_id, email)
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
  access_token = credentials.token
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
  # print('access_token = ' + access_token)
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