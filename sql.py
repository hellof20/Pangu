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
    try:
        sql="insert into deploy(solution_id,status,project_id,email,parameters) values('" + solution_id +"','new','" + project_id +"','" + email +"','" + json.dumps(parameters) +"');"
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except pymysql.Error as e:
        return str(e)
    else:
        return '创建部署任务成功'

def list_deploy_email(email): 
    conn.ping(reconnect=True)
    result = check_admin(email)
    if result == 1:
        sql = "select id,solution_id,JSON_EXTRACT(parameters,'$.version') as version,JSON_EXTRACT(parameters,'$.deploy_type'),project_id,email,create_time,update_time,status from deploy;"
    else:
        sql = "select id,solution_id,JSON_EXTRACT(parameters,'$.version') as version,JSON_EXTRACT(parameters,'$.deploy_type'),project_id,email,create_time,update_time,status from deploy where email = '" + email +"';"
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
    sql = "select distinct id, name from solution;"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    html_str = ''
    for i in json.loads(jsondata):
        id = i[0]
        name = i[1]
        html_str += "<option id = "+ id +" value ="+ id +">"+name+"</option>"
    return html_str

def list_solution_version(solution_id):
    conn.ping(reconnect=True)
    sql = "select version from solution where id = '" + solution_id + "';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    html_str = ''
    for i in json.loads(jsondata):
        version = i[0]
        html_str += "<option id = "+ version +" value ="+ version +">"+version+"</option>"
    return html_str    
    

def list_parameter(solution_id, email):
    conn.ping(reconnect=True)
    sql = "select id,name,description,type from parameters where show_on_ui = 1 and solution_id = (select distinct id from solution where id ='" + solution_id + "');"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    # print(json.loads(jsondata))
    html_str = ''
    version_str = ''
    deploy_type_str = ''

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
        if id == 'version':
            sql = "select version from solution where id = '" + solution_id + "';"
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            conn.commit()
            jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
            for i in json.loads(jsondata):
                version_str += '<option id ="version">' + i[0] +'</option>'
            html_str += '''
            <div style="margin-bottom: 10px;">
            Version:
            <select>
            ''' + version_str + '''
            </select>
            </div>
            '''
        elif id == 'deploy_type':
            html_str += '''
            <div style="margin-bottom: 10px;">
            Deploy_type:
            <select>
                <option id ="deploy_type" selected="selected">Terraform</option>
                <option id ="deploy_type">Bash</option>
            </select>
            </div>
            '''
        else:
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
    sql1 = "select parameters from deploy where id = '" + deploy_id +"';"
    cur = conn.cursor()
    cur.execute(sql1)
    sql1_result = cur.fetchone()[0]
    conn.commit()
    sql1_dict = json.loads(sql1_result)
    version = sql1_dict['version']
    deploy_type = sql1_dict['deploy_type']
    sql2 = "select id,url,tf_path,deploy_type,bash_path from solution where id = (select distinct solution_id from deploy a left join solution b on a.solution_id =b.id where a.id = '"+deploy_id+"') and deploy_type = '"+deploy_type+"' and version = '"+version+"';"
    cur.execute(sql2)
    sql2_result = cur.fetchone()
    conn.commit()
    return json.dumps(sql2_result)

def describe_deploy(deploy_id, solution_id):
    conn.ping(reconnect=True)
    sql1 = "select parameters from deploy where id = '" + deploy_id +"';"
    sql2 = "select id from parameters where solution_id = (select solution_id from deploy where show_on_ui = 1 and id = '"+deploy_id+"')"
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
    version_str = ''
    deploy_type_str = ''
    for k,v in sql2_dict.items():
        if k == 'project_id':
            html_str += '''
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">'''+ k +'''</span>
                </div>
                <input id='''+ k +''' value=''' + v +''' type="text" disabled="disabled" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
            </div>
            '''
        elif k == 'version':
            sql = "select version from solution where id = '" + solution_id + "';"
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            conn.commit()
            jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
            for i in json.loads(jsondata):
                if i[0] == v:
                    version_str += '<option id ="version" selected="selected" >' + i[0] +'</option>'
                else:
                    version_str += '<option id ="version">' + i[0] +'</option>'
            html_str += '''
            <div style="margin-bottom: 10px;">
            Version:
            <select>
            ''' + version_str + '''
            </select>
            </div>
            '''
        elif k=='deploy_type':
            deploy_type_data = ['Terraform','Bash']
            for i in deploy_type_data:
                if i == v:
                    deploy_type_str += '<option id ="deploy_type" selected="selected" >' + i +'</option>'
                else:
                    deploy_type_str += '<option id ="deploy_type">' + i +'</option>'
            html_str += '''
            <div style="margin-bottom: 10px;">
            Deploy_type:
            <select>
            ''' + deploy_type_str + '''
            </select>
            </div>
            '''            
        else:
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
    sql = "update deploy set parameters='"+json.dumps(parameters)+"',status='parameters_updated' where id='"+deploy_id+"';"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return 'success'