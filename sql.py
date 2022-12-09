import pymysql
import json
import os
import googleapiclient.discovery as discovery

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
        return 'Deploy Task Create Succes!'

def delete_task(deploy_id):
    conn.ping(reconnect=True)
    try:
        sql="delete from deploy where id = "+ deploy_id +";"
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except pymysql.Error as e:
        return str(e)
    else:
        return 'delete task succes!'


def list_deploy_email(email): 
    conn.ping(reconnect=True)
    result = check_admin(email)
    if result == 1:
        sql = "select id,solution_id,JSON_UNQUOTE(JSON_EXTRACT(parameters,'$.version')) as version, JSON_UNQUOTE(JSON_EXTRACT(parameters,'$.deploy_type')) as deploy_type,JSON_UNQUOTE(JSON_EXTRACT(parameters,'$.project_id')) as project_id,email,create_time,update_time,status from deploy;"
    else:
        sql = "select id,solution_id,JSON_UNQUOTE(JSON_EXTRACT(parameters,'$.version')) as version, JSON_UNQUOTE(JSON_EXTRACT(parameters,'$.deploy_type')) as deploy_type,JSON_UNQUOTE(JSON_EXTRACT(parameters,'$.project_id')) as project_id,email,create_time,update_time,status from deploy where email = '" + email +"';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    # print(json.loads(jsondata))
    dd = []
    for i in json.loads(jsondata):
        i.append('''
        <button style='margin-top: 5px;' id="apply" type="button" class="btn btn-primary btn-sm" >Deploy</button>
        <button style='margin-top: 5px;' id="destroy" type="button" class="btn btn-primary btn-sm" >Destroy</button>
        <button style='margin-top: 5px;' id="deploylog" type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#exampleModalLong">Log</button>
        <button style='margin-top: 5px;' id="describe_deploy" type="button" class="btn btn-primary btn-sm"  data-toggle="modal" data-target="#detail_data_pop">Edit</button>
        <button style='margin-top: 5px;' id="delete" type="button" class="btn btn-primary btn-sm">Delete</button>
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

def list_parameter(solution_id, email, credentials):
    conn.ping(reconnect=True)
    sql = "select id,name,description,type from parameters where show_on_ui = 1 and solution_id = (select distinct id from solution where id ='" + solution_id + "');"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    # print(json.loads(jsondata))
    html_str = ''
    html_str_1 = '<h5>Solution Parameters</h5>'
    head3_html_str = '<h5>Deploy Parameters</h5>'
    html_str_2 = ''
    project_html_str = ''

    # get solution supported deploy type
    deploy_type_sql = "select deploy_type from solution where id = '" + solution_id +"';"
    cur = conn.cursor()
    cur.execute(deploy_type_sql)
    result = cur.fetchall()
    conn.commit()
    deploy_type_str = ''
    deploy_type_data = json.dumps(result, indent=4, sort_keys=True, default=str)
    for i in json.loads(deploy_type_data):
        deploy_type_str += '<option id ="deploy_type">' + i[0] +'</option>'

    # get if need oauth
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
            html_str_1 += '''
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Version(Optional)</span>
                </div>
                <input id="version" type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
            </div>            
            '''
        elif id == 'deploy_type':
            html_str_1 += '''
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text">Deploy_type</span>
                    </div>
                    <select> ''' + deploy_type_str +'''</select>
                </div>
            '''         
        # elif id == 'project_id':
        #     resourcemanager = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
        #     project_result = resourcemanager.projects().list().execute()
        #     project_str = ''
        #     for dict in project_result['projects']:
        #         project_str += '<option id ="project_id" value='+ dict['projectId'] +'>' + dict['name'] +'</option>'
        #     project_html_str += '''
        #         <div class="input-group mb-3">
        #             <div class="input-group-prepend">
        #                 <span class="input-group-text">'''+name+'''</span>
        #             </div>
        #             <select> ''' + project_str +'''</select>
        #         </div>
        #     '''
        else:
            html_str_2 += '''
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">'''+name+'''</span>
                </div>
                <input id='''+id+''' type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
            </div>
            '''
    html_str += html_str_1 + '<hr />' + head3_html_str + html_str_2
    return html_str

# def get_deploy(deploy_id):
#     conn.ping(reconnect=True)
#     sql1 = "select parameters from deploy where id = '" + deploy_id +"';"
#     cur = conn.cursor()
#     cur.execute(sql1)
#     sql1_result = cur.fetchone()[0]
#     conn.commit()
#     sql1_dict = json.loads(sql1_result)
#     print(sql1_dict)
#     version = sql1_dict['version']
#     deploy_type = sql1_dict['deploy_type']
#     sql2 = "select id,url,tf_path,deploy_type,bash_path from solution where id = (select distinct solution_id from deploy a left join solution b on a.solution_id =b.id where a.id = '"+deploy_id+"') and deploy_type = '"+deploy_type+"';"
#     cur.execute(sql2)
#     sql2_result = cur.fetchone()
#     conn.commit()
#     sql_result = sql2_result + (version,)
#     return json.dumps(sql_result)

def get_deploy(deploy_id):
    conn.ping(reconnect=True)
    sql = '''
        select a.id,a.url,a.deploy_path ,b.deploy_type, b.parameters  from solution a right join (
        select solution_id,parameters, JSON_UNQUOTE(JSON_EXTRACT(parameters,'$.deploy_type')) as deploy_type 
        from deploy
        where id=''' + deploy_id + ''') b on a.id=b.solution_id and a.deploy_type =b.deploy_type
    '''
    cur = conn.cursor()
    cur.execute(sql)
    sql_result = cur.fetchone()
    print(sql_result)
    return json.dumps(sql_result)

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
    html_str_1 = '<h5>Solution Parameters</h5>'
    html_str_2 = '<h5>Deploy Parameters</h5>'
    deploy_type_str = ''
    for k,v in sql2_dict.items():
        if k == 'version':
            html_str_1 += '''
            Version(Optional):
            <input id="version" type="text" values = ''' + v + '''>
            '''
        elif k=='deploy_type':
            deploy_type_data = ['Terraform','Bash']
            for i in deploy_type_data:
                if i == v:
                    deploy_type_str += '<option id ="deploy_type" selected="selected" >' + i +'</option>'
                else:
                    deploy_type_str += '<option id ="deploy_type">' + i +'</option>'
            html_str_1 += '''
            <div style="margin-bottom: 10px;">
            Deploy_type:
            <select>
            ''' + deploy_type_str + '''
            </select>
            </div>
            '''
        else:
            html_str_2 += '''
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">'''+ k +'''</span>
                </div>
                <input id='''+ k +''' value=''' + v +''' type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
            </div>
            '''
    html_str = html_str_1 + '<hr />' + html_str_2    
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