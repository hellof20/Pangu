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


def insert_deploy(solution_id,email,parameters):
    conn.ping(reconnect=True)
    sql="insert into deploy(solution_id,status,email,parameters) values('" + solution_id +"','empty','" + email +"','" + json.dumps(parameters) +"');"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return '创建任务成功'

def list_deploy_email(email): 
    conn.ping(reconnect=True)
    result = check_admin(email)
    if result == 1:
        sql = "select id,solution_id,email,create_time,update_time,status from deploy;"
    else:
        sql = "select id,solution_id,email,create_time,update_time,status from deploy where email = '" + email +"';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    # print(json.loads(jsondata))
    dd = []
    for i in json.loads(jsondata):
        i.append('''
        <button id="apply" type="button" class="btn btn-primary btn-sm" >Deploy</button>
        <button id="destroy" type="button" class="btn btn-primary btn-sm">Destroy</button>
        <button id="upgrade" type="button" class="btn btn-primary btn-sm">Upgrade</button>
        <button id="deploylog" type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#exampleModalLong">Log</button>
        <button id="describe_deploy" type="button" class="btn btn-primary btn-sm"  data-toggle="modal" data-target="#detail_data_pop">Edit</button>
        ''')
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

def get_solution_scope(solution_id):
    conn.ping(reconnect=True)
    sql = "select scope from solution where id = '"+ solution_id +"';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    conn.commit()
    return result


def list_solution():
    conn.ping(reconnect=True)
    sql = "select id, name from solution;"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    # print(json.loads(jsondata))
    html_str = ''
    for i in json.loads(jsondata):
        id = i[0]
        name = i[1]
        html_str += "<option id = "+ id +" value ="+ id +">"+name+"</option>"
    return html_str
    

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

    sql = "select if_need_oauth from solution where id = '" + solution_id +"';"
    cur = conn.cursor()
    cur.execute(sql)
    if_need_oauth = cur.fetchone()
    if if_need_oauth[0] == 1:
        html_str = "<div style='margin-bottom: 15px;'><a href=oauth?solution_id='"+ solution_id +"' title='Authorization'>Authorization is required</a></div>"
    for i in json.loads(jsondata):
        id = i[0]
        name = i[1]
        desc = i[2]
        type = i[3]
        html_str += '''
        <div class="input-group mb-3">
            <div class="input-group-prepend">
                <span class="input-group-text">'''+name+'''</span>
            </div>
            <input id='''+id+''' type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
        </div>
        '''
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
    sql1 = "select parameters from deploy where id = '" + deploy_id +"';"
    sql2 = "select id from parameters where solution_id = (select solution_id from deploy where id = '"+deploy_id+"')"
    sql1_dict = {}
    sql2_dict = {}
    
    cur = conn.cursor()
    cur.execute(sql1)
    sql1_result = cur.fetchone()[0]
    cur.execute(sql2)
    sql2_result = cur.fetchall()
    conn.commit()
    
    for i in sql2_result:
        sql2_dict[i[0]]='null'

    sql1_dict = json.loads(sql1_result)

    for k,v in sql2_dict.items():
        if k in sql1_dict:
            sql2_dict[k] = sql1_dict[k]

    html_str = ''
    for k,v in sql2_dict.items():
        print(k + ":" + v)
        html_str += '''
        <div class="input-group mb-3">
            <div class="input-group-prepend">
                <span class="input-group-text">'''+ k +'''</span>
            </div>
            <input id='''+ k +''' value=''' + v +''' type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
        </div>
        '''
    return html_str

def update_deploy_status(deploy_id, status):
    conn.ping(reconnect=True)
    sql = "update deploy set status='"+status+"' where id='"+deploy_id+"';"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return 'updated status'


def update_parameters(deploy_id, parameters):
    conn.ping(reconnect=True)
    sql = "update deploy set parameters='"+json.dumps(parameters)+"' where id='"+deploy_id+"';"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return 'success'    