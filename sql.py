import pymysql
import json
import os

conn = pymysql.connect(
    host=os.environ.get('host'),
    user=os.environ.get('user'),
    password=os.environ.get('password'),
    database='ads',
    port=3306,
    charset='utf8mb4',
    connect_timeout=1)


def insert_deploy(solution_id,project_id,email,parameters):
    sql="insert into deploy(solution_id,status,project_id,email,parameters) values('" + solution_id +"','empty','" + project_id +"','" + email +"','" + json.dumps(parameters) +"');"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return '创建任务成功'

def list_deploy_email(email):  
    sql = "select id,solution_id,project_id,email,create_time,update_time,status from deploy where email = '" + email +"';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    print(json.loads(jsondata))
    dd = []
    for i in json.loads(jsondata):
        i.append('<button id="apply" >Deploy</button> <button id="destroy">Destroy</button> <button id="upgrade">Upgrade</button> <button id="deploylog">Log</button> <button id="describe_deploy">Detail</button>')
        dd.append(i)
    return json.dumps(dd)

def list_solution():  
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

def list_parameter(solution_id):
    sql = "select b.id,b.name,b.description from solution a left join parameters b on a.id = b.solution_id where solution_id = '" + solution_id + "' and show_on_ui = 1;"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    print(json.loads(jsondata))
    html_str = ''
    for i in json.loads(jsondata):
        id = i[0]
        name = i[1]
        desc = i[2]
        print('desc = ' + desc)
        html_str += "<div class='form-item'><span><a href=# title='"+desc+"'>"+name+":</a></span><input type='text' name="+ id +" id="+ id +" /></div>"
    return html_str

def get_deploy(deploy_id):   
    sql = "select a.solution_id,b.url from deploy a left join solution b on a.solution_id =b.id where a.id = '" + deploy_id +"';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    conn.commit()
    print(json.dumps(result))
    return json.dumps(result)

def describe_deploy(deploy_id):   
    sql = "select parameters from deploy where id = '" + deploy_id +"';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    conn.commit()
    print(json.dumps(result))
    return json.dumps(result)

def update_deploy_status(deploy_id, status):   
    sql = "update deploy set status='"+status+"' where id='"+deploy_id+"';"
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return 'updated status'