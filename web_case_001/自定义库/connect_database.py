#coding=utf-8
import MySQLdb,os
def kill_process(name):
    """
    专杀windows进程，传入进程的名称
    """
    os.system("taskkill /f /im   "+name+"  >nul  2>nul ")

def connect_to_mysqldb(myhost, myport, myuser, mypasswd, mydb):
    """
    连接mysql数据库
    """
    conn = MySQLdb.connect(
        host=myhost,
        port=int(myport),
        user=myuser,
        passwd=mypasswd,
        db=mydb,
        charset="utf8")
    return conn


def excute_mysql_str(conn, mysql_str, parameters=None):
    """
    执行sql语句，并且返回查询结果
    :param conn: 
    :param mysql_str: 
    :param parameters: 
    :return: 
    """
    cur = conn.cursor()
    info = []
    if parameters:
        conditions = parameters
        if type(conditions) in (int, float):
            conditions = str(conditions)
        condition_list = analysis_paralist(conditions)
        rs = cur.execute(mysql_str, condition_list)
        conn.commit()
        info = cur.fetchmany(rs)
    else:
        rs = cur.execute(mysql_str)
        conn.commit()
        info = cur.fetchmany(rs)
    cur.close()
    conn.close()
    return info


def analysis_paralist(conditions):
    """
    分析sql 后面跟的参数
    :param conditions: 
    :return: 
    """
    condition_list = []
    if conditions.find("|") == -1:
        condition_list.append(conditions.encode('utf8'))
    else:
        condition_split = conditions.split('|')
        for split_str in condition_split:
            condition_list.append(split_str.encode('utf8'))
    return condition_list


