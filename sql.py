import pymysql
import json
import os
import googleapiclient.discovery as discovery
from loguru import logger
import sys

class Database:
    """Database connection class."""
    def __init__(self):
        self.host = os.environ.get('host')
        self.username = os.environ.get('user')
        self.password = os.environ.get('password')
        self.port = 3306
        self.dbname = os.environ.get('db')
        self.conn = None

    def open_connection(self):
        """Connect to MySQL Database."""
        try:
            if self.conn is None:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.username,
                    passwd=self.password,
                    db=self.dbname,
                    connect_timeout=5,
                    charset='utf8mb4'
                )
        except pymysql.MySQLError as e:
            logger.error(e)
            sys.exit()
        finally:
            logger.info('Connection opened successfully.')

    def run_query(self, query):
        """Execute SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                if 'select' in query:
                    records = []
                    cur.execute(query)
                    result = cur.fetchall()
                    for row in result:
                        records.append(row)
                    cur.close()
                    return records
                result = cur.execute(query)
                self.conn.commit()
                affected = f"{cur.rowcount} rows affected."
                cur.close()
                return affected
        except pymysql.MySQLError as e:
            logger(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                logger.info('Database connection closed.')

db = Database()
db2 = Database()


def insert_deploy(solution_id,project_id,email,version,deploy_type):
    sql="insert into deploy(solution_id,status,project_id,email,version,deploy_type) values('"+solution_id+"','new','"+project_id+"','"+email+"','"+version+"','"+deploy_type+"');"
    db.run_query(sql)
    deploy_id = db.run_query("select max(id) from deploy where email='"+email+"' and project_id='"+project_id+"' and solution_id='"+solution_id+"'")[0][0]
    return str(deploy_id)


def get_solution(solution_id,deploy_type):
    print(solution_id)
    print(deploy_type)
    sql = "select url,deploy_path from solution where id='"+ solution_id +"' and deploy_type='"+ deploy_type +"' "
    result = db.run_query(sql)
    print(result)
    return result


def delete_task(deploy_id):
    sql="delete from deploy where id = "+ deploy_id +";"
    db.run_query(sql)
    return 'Delete task succes!'


def list_deploy_email(email): 
    result = check_admin(email)
    if result == 1:
        sql = "select id,solution_id,version, deploy_type,project_id,email,create_time,update_time,status from deploy;"
    else:
        sql = "select id,solution_id,version, deploy_type,project_id,email,create_time,update_time,status from deploy where email = '" + email +"';"
    result = db.run_query(sql)
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    dd = []
    for i in json.loads(jsondata):
        i.append('''
        <button style='margin-top: 5px;' id="deploylog" type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#exampleModalLong">Log</button>
        <button style='margin-top: 5px;' id="delete" type="button" class="btn btn-primary btn-sm">Delete</button>
        ''')
        dd.append(i)
    return json.dumps(dd)


def list_solution_detail():
    sql = "select distinct id,name,author,concat('<a href=',url,'>','link','</a>'),concat('<a href=',guide_url,'>','link','</a>') from solution;"
    result = db2.run_query(sql)
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    dd = []
    for i in json.loads(jsondata):
        i.append('''
        <button id="create_task_from_solution" type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">Deploy</button>
        ''')
        dd.append(i)
    return json.dumps(dd)


def list_parameter(solution_id, email, credentials):
    sql = "select id,name,description,type,default_value from parameters where show_on_ui = 1 and solution_id = (select distinct id from solution where id ='" + solution_id + "');"
    result = db.run_query(sql)
    jsondata = json.dumps(result, indent=4, sort_keys=True, default=str)
    html_str = ''
    html_str_1 = '<h5>Solution Parameters</h5>'
    head3_html_str = '<h5>Deploy Parameters</h5><div id="deploy_parameters">'
    html_str_2 = ''
    project_html_str = ''
    disclaimer_str = "<input type='checkbox' id='disclaimer' name='disclaimer'> I've read and accepted the <a href=/disclaimer>disclaimer</a>"

    # get solution supported deploy type
    deploy_type_sql = "select deploy_type from solution where id = '" + solution_id +"';"
    result = db.run_query(deploy_type_sql)
    deploy_type_str = ''
    deploy_type_data = json.dumps(result, indent=4, sort_keys=True, default=str)
    for i in json.loads(deploy_type_data):
        deploy_type_str += '<option id ="deploy_type">' + i[0] +'</option>'

    # get if need oauth
    sql = "select if_need_oauth from solution where id = '" + solution_id +"';"
    result = db.run_query(sql)
    if_need_oauth = result[0][0]
    if if_need_oauth == 1:
        html_str = "<div style='margin-bottom: 15px;'><a href=oauth?solution_id='"+ solution_id +"' title='Authorization'>Authorization is required</a></div>"
    for i in json.loads(jsondata):
        id = i[0]
        name = i[1]
        desc = i[2]
        type = i[3]
        default_value = i[4]
        if default_value is None:
            default_value = ""
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
        else:
            html_str_2 += '''
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">'''+name+'''</span>
                </div>
                <input id='''+id+''' type="text" value = "'''+default_value+'''" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
            </div>
            '''
    html_str += html_str_1 + '<hr />' + head3_html_str + html_str_2 + '</div>' + disclaimer_str
    return html_str


def check_admin(email):     # 判断邮箱是否为管理员
    result = db.run_query("select email from admin_user where email = '" + email +"';")
    if len(result)==0:
        return 0
    else:
        return 1


def list_solution():
    sql = "select distinct id, name from solution;"
    result = db.run_query(sql)
    html_str = ''
    for i in result:
        id = i[0]
        name = i[1]
        html_str += "<option id = "+ id +" value ="+ id +">"+name+"</option>"
    return html_str


def update_deploy_status(deploy_id, status):
    sql = "update deploy set status='"+status+"' where id='"+deploy_id+"';"
    db.run_query(sql)
    return 'updated status'