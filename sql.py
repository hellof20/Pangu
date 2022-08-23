import pymysql
import json
import os

conn = pymysql.connect(
    host=os.environ.get('host'),
    user=os.environ.get('user'),
    password=os.environ.get('password'),
    database=os.environ.get('db'),
    port=3306,
    charset='utf8mb4',
    connect_timeout=1)


def insert_deploy(solution_id,project_id,email,parameters):
    conn.ping(reconnect=True)
    sql="insert into deploy(solution_id,status,project_id,email,parameters) values('" + solution_id +"','empty','" + project_id +"','" + email +"','" + json.dumps(parameters) +"');"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return '创建任务成功'

def list_deploy_email(email): 
    conn.ping(reconnect=True)
    result = check_admin(email)
    if result == 1:
        sql = "select id,solution_id,project_id,email,create_time,update_time,status from deploy;"
    else:    
        sql = "select id,solution_id,project_id,email,create_time,update_time,status from deploy where email = '" + email +"';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    # print(json.loads(jsondata))
    dd = []
    for i in json.loads(jsondata):
        i.append('<button id="apply" >Deploy</button> <button id="destroy">Destroy</button> <button id="upgrade">Upgrade</button> <button id="deploylog">Log</button> <button id="describe_deploy">Detail</button>')
        dd.append(i)
    return json.dumps(dd)

def check_admin(email):     # 判断邮箱是否为管理员
    conn.ping(reconnect=True)
    sql = "select email from admin_user where email = '" + email +"';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    if result is not None:
        return 1
    else:
        return 0

def get_scope():
    conn.ping(reconnect=True)
    sql = "select scope from permission"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    scopes = []
    for i in json.loads(jsondata):
        scopes.append(i[0])
    return scopes


def list_solution():
    conn.ping(reconnect=True)
    sql = "select id, name from solution;"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    # print(json.loads(jsondata))
    dd = []
    for i in json.loads(jsondata):
        id = i[0]
        name = i[1]
        dd.append("<option id = "+ id +" value ="+ id +">"+name+"</option>")
    return json.dumps(dd)
    

def list_parameter(solution_id, email):
    conn.ping(reconnect=True)
    sql = "select b.id,b.name,b.description,b.type from solution a left join parameters b on a.id = b.solution_id where solution_id = '" + solution_id + "' and show_on_ui = 1;"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    # print(json.loads(jsondata))
    html_str = ''
    
    sql1 = "select if_need_oauth from solution where id = '" + solution_id +"';"
    sql2 = "select refresh_token from user_solution_oauth where solution_id = '" + solution_id +"' and email = '" + email +"';"
    cur = conn.cursor()
    cur.execute(sql1)
    if_need_oauth = cur.fetchone()
    cur.execute(sql2)
    if_exist_oauth = cur.fetchone()
    # todo
    # 判断是否需要oauth
    # 判断user_solution_oauth表中是否存在refresh_token
    if json.dumps(if_need_oauth)[1] == '1' and if_exist_oauth is None:
        html_str = "<div class='form-item'><span>client_id</span><input type='text' name='client_id' id='client_id' /></div><div class='form-item'><span>client_secret</span><input type='text' name='client_secret' id='client_secret' /></div> <button id ='get_authorize_url' style='margin-top :20px;' onclick='get_authorize_url()'>Authorization</button> <div class='form-item'><span style=' margin-bottom: 20px;'>how to generate client id and client secret <a href='#'>guide</a></span></div>"
    else:
        for i in json.loads(jsondata):
            id = i[0]
            name = i[1]
            desc = i[2]
            type = i[3]
            html_str += "<div class='form-item'><span><a href=# title='"+desc+"'>"+name+":</a></span><input type='text' name="+ id +" id="+ id +" /></div>"
        html_str += '<button id ="create" style="margin-top :20px; margin-bottom: 20px;" onclick="create()">CreateDeployTask</button>'        

    return html_str

def get_deploy(deploy_id):
    conn.ping(reconnect=True) 
    sql = "select a.solution_id,b.url,b.tf_path from deploy a left join solution b on a.solution_id =b.id where a.id = '" + deploy_id +"';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    conn.commit()
    # print(json.dumps(result))
    return json.dumps(result)

def describe_deploy(deploy_id):
    conn.ping(reconnect=True)
    sql = "select parameters from deploy where id = '" + deploy_id +"';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    conn.commit()
    # print(json.dumps(result))
    return json.dumps(result)

def update_deploy_status(deploy_id, status):
    conn.ping(reconnect=True)
    sql = "update deploy set status='"+status+"' where id='"+deploy_id+"';"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return 'updated status'


def insert_client_id_secret_token(email, solution_id,client_id, client_secret, refresh_token):
    conn.ping(reconnect=True)
    sql = "insert into user_solution_oauth(email, solution_id,client_id, client_secret, refresh_token) values('"+email+"', '"+solution_id+"', '"+client_id+"', '"+client_secret+"', '"+refresh_token+"');"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return 'inserted email client_id client_secret refresh_token'