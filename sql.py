import pymysql
import json

conn = pymysql.connect(
    host='127.0.0.1',
    user='pwm',
    password='szcb__123',
    database='ads',
    port=3306,
    charset='utf8mb4',
    connect_timeout=1)


def insert_deploy(solution_id,project_id):
    sql="insert into deploy(solution_id,status,project_id) values('"+ solution_id +"','new','"+ project_id +"');"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return '创建任务成功'

def list_deploy():   
    sql = "select id,solution_id,create_time,update_time,status from deploy;"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    dd = []
    for i in json.loads(jsondata):
        i.append('<button id="apply" >部署</button> <button id="destroy">删除</button> <button id="log">日志</button>')
        dd.append(i)
    return json.dumps(dd)

def get_deploy(deploy_id):   
    sql = "select a.solution_id,a.project_id,b.url from deploy a left join solution b on a.solution_id =b.id where a.id = '" + deploy_id +"';"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    print(json.dumps(result))
    return json.dumps(result)