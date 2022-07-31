# -*- coding: utf-8 -*-

import os,subprocess
import flask
import requests
from flask import request,render_template,send_file
import json
import sql

from python_terraform import *

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ['https://www.googleapis.com/auth/compute','https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email','openid']
API_SERVICE_NAME = 'compute'
API_VERSION = 'v1'

app = flask.Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'xxxxxxx'

@app.route('/')
def index():
  return render_template('auth.html')

@app.route('/ads')
def ads():
  return render_template('ads.html')

@app.route('/list_deploy_email', methods=['OPTIONS','GET','POST'])
def list_deploy_email():
  access_token = get_credentials()
  email = get_user_email(access_token)
  print('email='+email)
  result = sql.list_deploy_email(email)
  return result


@app.route('/apply', methods=['OPTIONS','GET','POST'])
def apply():
  access_token = get_credentials()
  DEPLOY_ID = request.form.get("deploy_id")
  data = json.loads(sql.get_deploy(DEPLOY_ID))
  url = data[2]
  PROJECT_ID = data[1]
  subprocess.Popen('export DEPLOY_ID=%s url=%s access_token=%s PROJECT_ID=%s && bash apply.sh' % (DEPLOY_ID,url,access_token,PROJECT_ID), shell=True )
  sql.update_deploy_status(DEPLOY_ID, 'deploying..')
  return "部署中。。。 请等待"


@app.route('/destroy', methods=['OPTIONS','GET','POST'])
def destroy():   
  access_token = get_credentials()
  DEPLOY_ID = request.form.get("deploy_id")
  data = json.loads(sql.get_deploy(DEPLOY_ID))
  url = data[2]
  PROJECT_ID = data[1]
  subprocess.Popen('export DEPLOY_ID=%s url=%s access_token=%s PROJECT_ID=%s && bash destroy.sh' % (DEPLOY_ID,url,access_token,PROJECT_ID), shell=True )
  sql.update_deploy_status(DEPLOY_ID, 'deleting..')
  return "删除中。。。 请等待"


@app.route('/upgrade', methods=['OPTIONS','GET','POST'])
def upgrade():
  access_token = get_credentials()
  DEPLOY_ID = request.form.get("deploy_id")
  data = json.loads(sql.get_deploy(DEPLOY_ID))
  url = data[2]
  PROJECT_ID = data[1]
  subprocess.Popen('export DEPLOY_ID=%s url=%s access_token=%s PROJECT_ID=%s && bash upgrade.sh' % (DEPLOY_ID,url,access_token,PROJECT_ID), shell=True )
  sql.update_deploy_status(DEPLOY_ID, 'upgrading..')
  return '更新中。。。请等待'


@app.route('/deploylog', methods=['OPTIONS','GET','POST'])
def deploylog():
  DEPLOY_ID = request.form.get("deploy_id")
  try:
    if os.path.exists('/tmp/%s/tf-tutorial/tf.log' %DEPLOY_ID):
      return send_file('/tmp/%s/tf-tutorial/tf.log' %DEPLOY_ID)
    else:
      return '日志文件不存在'
  except:
    return '获取日志出错'


@app.route('/create', methods=['OPTIONS','GET','POST'])
def create():
    access_token = get_credentials()
    PROJECT_ID = request.form.get("project_id")
    BUCKET_NAME = request.form.get("bucket_name")
    SOLUTION = request.form.get("solution")
    email = get_user_email(access_token)
    sql.insert_deploy(SOLUTION,PROJECT_ID,email)
    result = sql.list_deploy_email(email)
    return '创建部署任务成功'


@app.route('/authorize')
def authorize():
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True, _scheme='https')
  # authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
  authorization_url, state = flow.authorization_url(access_type='offline')
  print(authorization_url)
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
  return flask.redirect('/ads')


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
  print('access_token = ' + access_token)
  return access_token


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}        


def print_index_table():
  return ('<table>' +
          '<tr><td><a href="/apply">Test an API request</a></td>' +
          '<td>Submit an API request and see a formatted JSON response. ' +
          '    Go through the authorization flow if there are no stored ' +
          '    credentials for the user.</td></tr>' +
          '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
          '<td>Go directly to the authorization flow. If there are stored ' +
          '    credentials, you still might not be prompted to reauthorize ' +
          '    the application.</td></tr>' +
          '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
          '<td>Revoke the access token associated with the current user ' +
          '    session. After revoking credentials, if you go to the test ' +
          '    page, you should see an <code>invalid_grant</code> error.' +
          '</td></tr>' +
          '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
          '<td>Clear the access token currently stored in the user session. ' +
          '    After clearing the token, if you <a href="/test">test the ' +
          '    API request</a> again, you should go back to the auth flow.' +
          '</td></tr></table>')

if __name__ == '__main__':
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  app.run('0.0.0.0', 8080, debug=True)




  # bm = Terraform(working_dir='/tmp/%s/tf-tutorial' % DEPLOY_ID)
  # return_code, stdout, stderr = bm.destroy(force=IsNotFlagged, auto_approve=True, var={'project':PROJECT_ID,'access_token':access_token})
  # fo = open("/tmp/%s/tf-tutorial/tf.log"%DEPLOY_ID, "w")
  # if return_code == 0:
  #   sql.update_deploy_status(DEPLOY_ID,'new')
  #   fo.write(stdout)
  #   fo.close()
  #   return '删除成功'
  # else:
  #   fo.write(stdout)
  #   fo.write(stderr)
  #   fo.close()
  #   sql.update_deploy_status(DEPLOY_ID,'failed')
  #   return '删除失败' 

    # os.system('mkdir -p /tmp/%s && cd /tmp/%s && git clone %s' %(DEPLOY_ID, DEPLOY_ID, url))
  # subprocess.Popen('cd /tmp/%s/tf-tutorial && terraform init && terraform apply -auto-approve -var="project=%s" -var="access_token=%s" -no-color >> tf.log 2>&1' %(DEPLOY_ID,PROJECT_ID,access_token), shell=True)


  # subprocess.Popen('cd /tmp/%s/tf-tutorial && terraform apply -destroy -auto-approve -var="project=%s" -var="access_token=%s" -no-color >> tf.log 2>&1' %(DEPLOY_ID,PROJECT_ID,access_token), shell=True)


  # if 'credentials' not in flask.session:
  #   return '请授权'
  # else: 